from crypt import methods
import datetime
from io import BytesIO

from django import apps
from django.core.files import File
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from celery.result import AsyncResult
from apps.tender.emails import tender_send_participation_acknowledgment
from apps.core.pagination import PageNumberPagination

from apps.tender.models import (
    SupplierFinancialTotal, Tender, Category, Section, Question, SupplierResponse, MarkingScheme,
    QualityAssurance, QualityAssuranceQuestion, QualityAssuranceResponse, DueDiligence, DueDiligenceQuestion,
    DueDiligenceSupplier, SupplierCategoryScore, AwardLetter, RegretLetter, Item, SupplierFinancialResponse,
    ItemResponse, CategoryReport, Invitee, ClientDocument, SupplierTechnicalScore,
    FinancialRatio, QaTccResponse, QaIncorporationCertificateResponse, QaCr12Response, QaBusinessPermitResponse,
    QaNcaaResponse, QaPoisonsBoardResponse, QaNationalIdResponse, CustomLetter, DueDilligenceLetter,
)
from . import serializers
from .reports import (
    TenderQARankingReport, TenderInterimReport, DueDiligenceRankingReport, tender_participation_status,
    suppliers_list_report, tender_bidder_locations_report, tender_responsive_bidders_report,
    tender_non_responsive_bidders_report, tender_bidders_information_report, tender_evaluation_report_context,
    ConsolidatedTenderSummaryReport, job_qed_category_suppliers, download_current_suppliers, TenderSummaryReport,
    FinancialRatiosReport
    )
from .serializers import (
    JobListSerializer, JobCreateUpdateSerializer, CategoryListSerializer, CategoryCreateUpdateSerializer,
    SectionListSerializer, SectionCreateUpdateSerializer, QuestionListSerializer, QuestionCreateUpdateSerializer,
    MarkingSchemeSerializer, SRSerializer, QASerializer, QAQSerializer, QARSerializer
)

from .tasks import EvaluateTender, job_questions_upload, ZipQuestionFiles, upload_job_current_suppliers, \
    import_category_suppliers
from .utils import create_award_letter, create_regret_letter, tender_criteria_template_download, get_file, send_current_suppliers_letter_email
from .tasks import EvaluateTender, job_questions_upload, ZipQuestionFiles, submit_tender_rfq
from .utils import create_award_letter, create_regret_letter, tender_criteria_template_download,get_file
from ..buyer.models import Buyer
from ..core.utils import Render, get_file_path, weasy_pdf
from .tender_notifications import (
    broadcast_tender_job_notifications, send_tender_job_invite_sms, send_tender_job_invite_email, SendTenderEmailNotifications
)
from pathlib import Path
from django.db.models import Q


class JobView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return JobListSerializer
        else:
            return JobCreateUpdateSerializer

    def get_queryset(self):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']
        return Tender.objects.filter(company_id=company_id)

    @action(methods=['get'], detail=False, url_path=('search/(?P<key>.+)'))
    def search(self, request, key):
        jobs = self.get_queryset()
        jobs = jobs.filter(Q(title__icontains=key)|Q( unique_reference__icontains=key))

        page = self.paginate_queryset(jobs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        data_copy = request.data.copy()
        data_copy['company'] = company_id
        data_copy['created_by'] = request.user.id
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(methods=['get'], detail=False, url_path='job/details/letters/(?P<job_id>\d+)')
    def job_details_letters(self, request, job_id):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        jobs = Tender.objects.filter(
            id=job_id,
            company_id=company_id).first()

        serializer = serializers.LetterJobListSerializer(jobs, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='publish/(?P<job_id>\d+)')
    def publish_job(self, request, job_id):
        job = Tender.objects.filter(id=job_id).first()
        if job is not None:
            job.status = 'final'
            job.approved_by_id = request.user.id
            job.save()
            context = {
                "response_message": "Job published"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "Job already published"
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='download/criteria/template/(?P<job_id>\d+)')
    def download_criteria_template(self, request, job_id):
        job = Tender.objects.filter(id=job_id).first()
        if job:
            file_path = tender_criteria_template_download(job=job)
            context = {
                "response_message": "Template generated",
                "filepath": file_path
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='upload/criteria/template/(?P<job_id>\d+)')
    def upload_criteria_template(self, request, job_id):
        job = Tender.objects.filter(id=job_id).first()
        s = serializers.JobExcelSerializer(data=request.data, instance=job)

        if s.is_valid():
            s.save()
            c = job_questions_upload(job_id=job_id)
            context = {
                "response_message": "Criteria upload in progress",
                "messages": c["messages"]
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "response_message": "Criteria upload error",
                "errors": s.errors
            }
            return Response(context, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='upload/current/suppliers/(?P<job_id>\d+)')
    def upload_current_suppliers(self, request, job_id):
        job = Tender.objects.filter(id=job_id).first()
        s = serializers.JobUpdateCurrentSupplierSerializer(data=request.data, instance=job)

        if s.is_valid():
            s.save()
            c = upload_job_current_suppliers(job_id=job_id)
            context = {
                "response_message": "Current suppliers upload complete",
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "response_message": "Current suppliers upload error",
                "errors": s.errors
            }
            return Response(context, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='send/current_suppliers/letter/(?P<job_id>\d+)')
    def send_current_suppliers_letter(self, request, job_id):
        job = Tender.objects.filter(id=job_id).first()
        s = serializers.JobUpdateCurrentSupplierLetterSerializer(data=request.data, instance=job)

        if s.is_valid():
            s.save()
        context = send_current_suppliers_letter_email(job_id=job_id)
        context = {
            "response_message": "Emails sending in progress",
        }

        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path=('defaults'))
    def defaults(self, request):
        currencies = apps.apps.get_model('core', 'Currency').objects.order_by('id').all()
        category_types = apps.apps.get_model('core', 'CategoryType').objects.order_by('id').all()
        s = serializers.CurrencySerializer(currencies, many=True)
        d = serializers.CategoryTypeSerializer(category_types, many=True)
        context = {
            'currencies': s.data,
            'category_types': d.data
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/qa/report/(?P<job_id>\d+)')
    def run_qa_report(self, request, job_id):
        qa_ranking_report = TenderQARankingReport()
        context = qa_ranking_report.delay(job_id=job_id)
        context = {
            "response_message": "Report generation started",
            "task_id": context.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/interim/report/(?P<job_id>\d+)')
    def run_interim_report(self, request, job_id):
        report_instance = TenderInterimReport()
        result = report_instance.delay(job_id=job_id)
        context = {
            "response_message": "Report generation in progress",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/dd/ranking/report/(?P<job_id>\d+)')
    def run_dd_ranking_report(self, request, job_id):
        report_instance = DueDiligenceRankingReport()
        result = report_instance.delay(job_id=job_id)
        context = {
            "response_message": "Report generation in progress",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)\

    @action(methods=['get'], detail=False, url_path='run/participation/status/report/(?P<job_id>\d+)')
    def run_participation_status_report(self, request, job_id):
        result = tender_participation_status.delay(job_id=job_id)
        context = {
            "response_message": "Report generation in progress",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)\

    @action(methods=['get'], detail=False, url_path='run/supplier/details/report/(?P<job_id>\d+)')
    def run_supplier_details_report(self, request, job_id):
        result = suppliers_list_report.delay(job_id=job_id)
        context = {
            "response_message": "Report generation in progress",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/bidder/locations/report/(?P<job_id>\d+)')
    def run_bidder_locations_report(self, request, job_id):
        context = tender_bidder_locations_report.delay(job_id=job_id)
        context = {
            "response_message": "Report generation started",
            "task_id": context.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/responsive/bidders/report/(?P<job_id>\d+)')
    def run_responsive_bidders_report(self, request, job_id):
        context = tender_responsive_bidders_report.delay(job_id=job_id)
        context = {
            "response_message": "Report generation started",
            "task_id": context.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/non/responsive/bidders/report/(?P<job_id>\d+)')
    def run_non_responsive_bidders_report(self, request, job_id):
        context = tender_non_responsive_bidders_report.delay(job_id=job_id)
        context = {
            "response_message": "Report generation started",
            "task_id": context.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='category/suppliers/report/(?P<job_id>\d+)')
    def category_suppliers_report(self, request, job_id):
        result = job_qed_category_suppliers.delay(job_id=int(job_id))
        context = {
            'task_id': result.task_id,
            "response_message": "Report generation in progress",
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='run/current_suppliers/report/(?P<job_id>\d+)')
    def run_current_suppliers_report(self, request, job_id):
        context = download_current_suppliers.delay(job_id=job_id)
        context = {
            "response_message": "Report generation started",
            "task_id": context.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='upload/category/suppliers/(?P<job_id>\d+)')
    def upload_category_suppliers(self, request, job_id):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        instance = Tender.objects.filter(
            company_id=company_id, id=job_id
        ).first()
        s = serializers.TenderCatSupplierSerializer(data=request.data, instance=instance)
        if s.is_valid():
            s.save()
            result = import_category_suppliers.delay(job_id=int(job_id))
            context = {
                'task_id': result.task_id,
                "response_message": "Report generation in progress",
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "response_message": "Invalid, an error occurred",
                "errors": s.errors
            }
            return Response(context, status=status.HTTP_200_OK)

    #
    # @action(methods=['get'], detail=False, url_path='run/bidder/payments/report/(?P<job_id>\d+)')
    # def run_job_bidder_payments_report(self, request, job_id):
    #     context = job_bidder_payments_report.delay(job_id=job_id)
    #     context = {
    #         "response_message": "Report generation started",
    #         "task_id": context.task_id
    #     }
    #     return Response(context, status=status.HTTP_200_OK)
    #
    # @action(methods=['get'], detail=False, url_path='run/directors/report/(?P<job_id>\d+)')
    # def run_directors_report(self, request, job_id):
    #     context = directors_report.delay(job_id=job_id)
    #     context = {
    #         "response_message": "Report generation started",
    #         "task_id": context.task_id
    #     }
    #     return Response(context, status=status.HTTP_200_OK)


class CriteriaCountryView(viewsets.ModelViewSet):
    def get_queryset(self):
        return apps.apps.get_model('core', 'CriteriaCountry').objects.all().order_by('id')

    def get_serializer_class(self):
        return serializers.CriteriaCountrySerializer


class CategoryView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        elif self.action == 'retrieve':
            return serializers.CategoryRetrieveSerializer
        elif self.action == 'financial_details':
            return serializers.CategoryMinimizedDetailsSerializer
        else:
            return CategoryCreateUpdateSerializer

    def get_queryset(self):
        return Category.objects.filter(tender_id=self.kwargs['job_id'])

    @action(methods=['get'], detail=False, url_path=('search/(?P<key>.+)'))
    def search(self, request, job_id, key):
        categories = self.get_queryset()
        categories = categories.filter(Q(name__icontains=key)|Q( unique_reference__icontains=key))

        page = self.paginate_queryset(categories)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='sections/(?P<category_id>\d+)')
    def get_sections(self, request, job_id, category_id):
        sections = Section.objects.filter(category_id=category_id)
        serializer = serializers.SectionListSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='open/(?P<category_id>\d+)')
    def open(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        if category.is_open == True:
            context = {
                "response_message": "Category already open"
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            s = serializers.CategoryOpenSerializer(instance=category, data=request.data)
            if s.is_valid():
                s.save()
                context = {
                    "response_message": "Category opened successfully",
                    "data": s.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                    "response_message": "Data not valid"
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='close/(?P<category_id>\d+)')
    def close(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        if category.is_open == True:
            category.is_open = False
            category.closing_date = timezone.now()
            category.save()

            e = EvaluateTender()
            evaluate = e.delay(category_id=category_id)
            context = {
                "response_message": "Category closed successfully",
                "task_id": evaluate.task_id
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "response_message": "Invalid data"
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='run/report/(?P<category_id>\d+)/(?P<type>[\w\-]+)')
    def run_report(self, request, job_id, category_id, type="xls"):
        """
        Reports:    1. Bidders Information report as excel
                    2.  Evaluation report as pdf
        :param request:
        :param job_id:
        :return:
        """

        category = Category.objects.filter(id=category_id).first()
        if category is not None:
            participants = category.technical_participants
            sections = category.sections

            if type == "xls":
                data = {
                    "participants": participants, "category": category, "sections": sections
                }
                excel_path = tender_bidders_information_report(data=data)
                return excel_path
            elif type == "pdf":
                # sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                context['participant_count'] = len(participants)
                pdf = Render.render(
                    "tender/reports/technical_evaluation_report.html", context
                )
                pdf_file = BytesIO(pdf.content)
                category_report, created = CategoryReport.objects.update_or_create(
                    category_id=category_id,
                    defaults={
                        "technical_evaluation": File(pdf_file, "Technical_Evaluation_Report.pdf")
                    }
                )
                context = {
                    "file": category_report.technical_evaluation.url
                }
                return Response(context, status=status.HTTP_200_OK)
            elif type == "responses":
                sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": sorted_participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                return Render.render(
                    "qed_portal/prequalifications/prequal_evaluation_report_responses.html",
                    context,
                )
            elif type == "responsiveness":
                sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": sorted_participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                return Render.render(
                    "qed_portal/prequalifications/prequal_evaluation_report_responsive.html",
                    context,
                )
            elif type == "rank":
                sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": sorted_participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                return Render.render(
                    "qed_portal/prequalifications/prequal_evaluation_report_rank.html",
                    context,
                )
            elif type == "page1":
                sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": sorted_participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                return Render.render(
                    "qed_portal/prequalifications/prequal_evaluation_report_page1.html",
                    context,
                )
            else:
                sorted_participants = category.sorted_participants(participants)
                data = {
                    "participants": sorted_participants, "category": category, "sections": sections
                }
                context = tender_evaluation_report_context(data)
                return Render.render(
                    "qed_portal/prequalifications/prequal_evaluation_report_summary.html",
                    context,
                )
        else:
            return render(request, "qed_portal/404.html")
        pass

    @action(methods=['get'], detail=False, url_path='qualified/bidders/(?P<category_id>\d+)')
    def technical_qualified_bidders(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        pass_score = float(category.pass_score)
        # check if qa exists
        bidders = SupplierTechnicalScore.objects.filter(category_id=category_id, score__gte=pass_score)
        s = serializers.SupplierTechnicalScoreSerializer(bidders, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='unqualified/bidders/(?P<category_id>\d+)')
    def technical_unqualified_bidders(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        pass_score = float(category.pass_score)
        bidders = SupplierTechnicalScore.objects.filter(category_id=category_id, score__lt=pass_score)
        s = serializers.SupplierTechnicalScoreSerializer(bidders, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='technical/bidders/(?P<category_id>\d+)')
    def technical_participants(self, request, job_id, category_id):
        suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=category_id).only('supplier_id').values('supplier_id').distinct()
        )
        serializer = serializers.SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='technical/bidders/search/(?P<category_id>\d+)')
    def technical_participants_search(self, request, category_id, job_id):
        query = request.GET['query']
        
        queryset = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=category_id).only('supplier_id').values('supplier_id').distinct(),
                company_name__icontains=query
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.SupplierSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.SupplierSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='items/(?P<category_id>\d+)')
    def items(self, request, job_id, category_id):
        items = Item.objects.filter(category_id=category_id).order_by('number')
        serializer = serializers.ItemSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='all/bidders/(?P<category_id>\d+)')
    def participants(self, request, job_id, category_id):
        technical_participants = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=category_id).only('supplier_id').values('supplier_id').distinct()
        )
        financial_participants = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=ItemResponse.objects.filter(
                item__category_id=category_id).only('supplier_id').values('supplier_id')
        )
        participants=technical_participants|financial_participants
        page = self.paginate_queryset(participants)
        if page is not None:
            serializer = serializers.SupplierSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.SupplierSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='financial/bidders/(?P<category_id>\d+)')
    def financial_participants(self, request, job_id, category_id):
        # participants = SupplierFinancialResponse.objects.filter(category_id=category_id)
        participants = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=ItemResponse.objects.filter(
                item__category_id=category_id).only('supplier_id').values('supplier_id')
        )
        serializer = serializers.SupplierSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='minimized/details/(?P<category_id>\d+)')
    def financial_details(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        if category:
            s = serializers.CategoryMinimizedDetailsSerializer(category, many=False, context={'request': request})
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='refresh/scores/(?P<category_id>\d+)')
    def refresh_scores(self, request, job_id, category_id):
        category = Category.objects.filter(id=category_id).first()
        if not category.is_open:
            e = EvaluateTender()
            evaluate = e.delay(category_id=category_id)
            context = {
                "response_message": "Refreshing scores",
                "task_id": evaluate.task_id
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "response_message": "Category still open"
            }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='consolidated/tender/summary/(?P<category_id>\d+)')
    def consolidated_tender_summary_report(self, request, job_id, category_id):
        report = ConsolidatedTenderSummaryReport()
        result = report.delay(category_id=category_id)
        context = {
            "task_id": result.task_id,
            "response_message": "Report generation started",
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='multi-item/tender/summary/(?P<category_id>\d+)')
    def multi_item_tender_summary_report(self, request, job_id, category_id):
        report = TenderSummaryReport()
        result = report.delay(category_id=category_id)
        context = {
            "task_id": result.task_id,
            "response_message": "Report generation started",
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='invited/suppliers/(?P<category_id>\d+)')
    def invited_suppliers(self, request, job_id, category_id):
        invites = Invitee.objects.filter(category_id=category_id)
        page = self.paginate_queryset(invites)
        if page is not None:
            serializer = serializers.CategoryInviteSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.CategoryInviteSerializer(invites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='invite/from/email/(?P<category_id>\d+)')
    def invite_from_email(self, request, job_id, category_id, ):
        serializer = serializers.InviteBidderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
        context = {
            'response_message': 'Invite from email successful'
        }
        return Response(context, status=status.HTTP_200_OK)


class SectionView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Section.objects.filter(category_id=self.kwargs['category_id']).order_by('id')

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve' or self.action == 'section_search':
            return SectionListSerializer
        else:
            return SectionCreateUpdateSerializer
            
    @action(methods=['get'], detail=False, url_path='search')
    def section_search(self, request, category_id):
        query = request.GET['query']
        queryset = Section.objects.filter(
            category_id=category_id, name__icontains=query, trans_name__icontains=query,
            description__icontains=query
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class QuestionView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    def get_queryset(self):
        return Question.objects.filter(section_id=self.kwargs['section_id'])

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.QuestionListSerializer
        elif self.action == 'retrieve':
            return serializers.QuestionRetrieveSerializer
        else:
            return QuestionCreateUpdateSerializer

    @action(methods=['get'], detail=False, url_path='search')
    def search(self, request, section_id):
        query = request.GET['query']
        queryset = Question.objects.filter(
            Q(description__icontains=query) | Q(description__icontains=query),
            section_id=section_id
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class MarkingSchemeView(viewsets.ModelViewSet):
    def get_queryset(self):
        return MarkingScheme.objects.filter(question_id=self.kwargs['question_id'])

    def get_serializer_class(self):
        return MarkingSchemeSerializer


class SupplierResponseView(viewsets.ModelViewSet):
    def get_queryset(self):
        supplier_response = SupplierResponse.objects.filter(
            question_id=self.kwargs['question_id'], supplier_id=self.kwargs['supplier_id']
        )
        return supplier_response

    def get_serializer_class(self):
        return SRSerializer


class QAView(viewsets.ModelViewSet):
    def get_queryset(self):
        return QualityAssurance.objects.filter(category_id=self.kwargs['category_id'])

    def get_serializer_class(self):
        return QASerializer

    @action(methods=['get'], detail=False, url_path='sections')
    def get_sections(self, request, category_id):
        sections = Section.objects.filter(category_id=category_id, question__is_qa=True).distinct()
        s = SectionListSerializer(sections, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='section/questions/(?P<section_id>\d+)')
    def get_section_questions(self, request, category_id, section_id):
        questions = QualityAssuranceQuestion.objects.filter(question__is_qa=True, question__section_id=section_id)
        s = QAQSerializer(questions, many=True)
        return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='submit/instructions/(?P<question_id>\d+)')
    def submit_instructions(self, request, category_id, question_id):
        data = request.data.copy()
        quality_assurance = QualityAssurance.objects.filter(category_id=category_id).first()
        if quality_assurance is not None:
            data[quality_assurance] = quality_assurance.id

            qaq = QualityAssuranceQuestion.objects.filter(question_id=question_id).first()
            instance = serializers.QAQSerializer(data=data, instance=qaq)
            if instance.is_valid():
                instance.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path='section/questions/(?P<section_id>\d+)/(?P<participant_id>\d+)')
    def get_section_questions_participant_response(self, request, category_id, section_id, participant_id):
        section = Section.objects.filter(id=section_id).first()
        s = serializers.QaSectionQuestionsSupplierResponse(section, many=False, context={'participant_id': participant_id})
        return Response(s.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='submit/response/(?P<qaq_id>\d+)')
    def submit_response(self, request, category_id, qaq_id):
        data = request.data.copy()
        user = request.user.id

        qa_question = QualityAssuranceQuestion.objects.filter(
            id=qaq_id).prefetch_related('question').first()
        question = qa_question.question
        section = question.section
        supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id=data['supplier']).first()

        if data['outcome'] == 'Pass':
            if section.name == "Financial Ratios":
                data['score_after_qa'] = question.supplier_financial_ratio_score(supplier=supplier)
            else:
                data['score_after_qa'] = question.max_score
        elif data['outcome'] == 'Fail':
            data['score_after_qa'] = 0
        elif data['outcome'] == 'Subjective':
            if data['score_after_qa'] != '' and data['score_after_qa'] != ' ':
                data['score_after_qa'] = data['score_after_qa']
            else:
                data['score_after_qa'] = 0
        else:
            data['score_after_qa'] = 0

        data['created_by'] = user
        instance = QualityAssuranceResponse.objects.filter(
            quality_assurance_question_id=qaq_id,
            supplier_id=int(data['supplier'])
        ).first()

        if question.short_description.lower() == "Tax compliance".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data["date"]
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=data['supplier'], quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=data["date"],
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaTccResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "pin_number": data["number"], "pin_number_outcome": data["pin_number_outcome"],
                    "company_name": data["company_name"], "expiry_date": data["date"],
                    "expiry_date_outcome": data["expiry_date_outcome"]
                }
            )
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "CR12 Certificate or equivalent".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data['date']
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaCr12Response.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "company_number": data["number"], "document_date": data["date"],
                    "company_number_outcome": data["company_number_outcome"],
                    "directors_outcome": data["directors_outcome"]
                }
            )
            # "Company registration certificate number"
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "Business permit".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data['date']
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaBusinessPermitResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "business_id": data["number"], "date": data["date"],
                    "business_name": data["business_name"], "business_name_outcome": data["business_name_outcome"]
                }
            )
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "PIN certificate".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = datetime.datetime.now()
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaPinCertificateResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "pin_number": data["number"], "tax_pin_outcome": data["tax_pin_outcome"],
                }
            )
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "NCA Registration certificate".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data['date']
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaNcaaResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "serial_number": data["number"], "expiry_date": data["date"],
                    "expiry_date_outcome": data["expiry_date_outcome"]
                }
            )
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "Pharmacy and poisons board License".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data['date']
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaPoisonsBoardResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "expiry_date": data["date"],
                    "company_name": data["company_name"],
                    "company_name_outcome": data["company_name_outcome"],
                    "expiry_date_outcome": data["expiry_date_outcome"]
                }
            )
            return Response(status=status.HTTP_200_OK)
        elif question.short_description.lower() == "Registration certificate".lower():
            if instance is not None:
                instance.number = data["number"]
                instance.outcome = data["outcome"]
                instance.date = data['date']
                instance.score_after_qa = data["score_after_qa"]
                instance.comment = data["comment"]
                instance.save()
            else:
                instance = QualityAssuranceResponse.objects.create(
                    supplier_id=int(data['supplier']), quality_assurance_question_id=qaq_id,
                    number=data["number"], outcome=data["outcome"], date=datetime.datetime.now(),
                    score_after_qa=data["score_after_qa"], comment=data["comment"]
                )

            QaIncorporationCertificateResponse.objects.update_or_create(
                qa_response_id=instance.id,
                defaults={
                    "company_name": data["company_name"],
                    "company_name_outcome": data["company_name_outcome"],
                    "company_number": data["number"],
                    "company_number_outcome": data["company_number_outcome"]
                }
            )
            return Response(status=status.HTTP_200_OK)
        else:
            if instance is not None:
                serializer = QARSerializer(data=data, instance=instance)
            else:
                serializer = QARSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='ratios/qa/(?P<participant_id>\d+)')
    def submit_ratios(self, request, category_id, participant_id):
        instance  = FinancialRatio.objects.filter(section__category_id=category_id, supplier_id=participant_id).first()

        if instance is not None:
            s = serializers.FinancialRatioSerializer(data=request.data, instance=instance, context={'request': request})
        else:
            s = serializers.FinancialRatioSerializer(data=request.data, context={'request': request})

        if s.is_valid():
            s.save()
            context = {
                "response_message": "Ratios updated"
            }
            return Response(status=status.HTTP_200_OK)
        else:
            context = {
                "errors": s.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    # @action(methods=['get'], detail=False, url_path='sections/questions/instructions')
    # def qa_sections_questions_instructions(self, request, category_id):
    #     sections = Section.objects.filter(category_id=category_id)
    #     data = QaSectionQuestionInstructions(sections, many=True)
    #     return Response(data, status=status.HTTP_200_OK)


class QAQView(viewsets.ModelViewSet):
    def get_queryset(self):
        return QualityAssuranceQuestion.objects.filter(quality_assurance_id=self.kwargs['qa_id'])

    def get_serializer_class(self):
        return QAQSerializer


class QARView(viewsets.ModelViewSet):
    def get_queryset(self):
        responses = QualityAssuranceResponse.objects.filter(
            quality_assurance_question__quality_assurance_id=self.kwargs['qa_id']
        )
        return responses

    def get_serializer_class(self):
        return QARSerializer


class DDView(viewsets.ModelViewSet):
    def get_queryset(self):
        return DueDiligence.objects.filter(category_id=self.kwargs['category_id'])

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.DueDiligenceListSerializer
        elif self.action == 'create':
            return serializers.DueDiligenceCreateSerializer
        return serializers.DueDiligenceListSerializer

    @action(methods=['get'], detail=False, url_path='participants')
    def dd_participants(self, request, category_id):
        participants = DueDiligenceSupplier.objects.filter(
            due_diligence__category_id=category_id)
        serializer = serializers.DueDiligenceSupplierSerializer(participants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='participant/(?P<participant_id>\d+)')
    def dd_participant(self, request, category_id, participant_id):
        participants = DueDiligenceSupplier.objects.filter(
            due_diligence__category_id=category_id, id=participant_id).first()
        serializer = serializers.DueDiligenceSupplierSerializer(participants, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='questions/(?P<participant_id>\d+)')
    def dd_participants_questions(self, request, category_id, participant_id):
        questions = DueDiligenceQuestion.objects.filter(
            due_diligence_supplier_id=participant_id, due_diligence_supplier__due_diligence__category_id=category_id
        )
        dd_supplier = DueDiligenceSupplier.objects.filter(id=participant_id).first()
        context = {
            "questions": serializers.DueDiligenceQuestionSerializer(questions, many=True).data,
            "participant": serializers.DueDiligenceSupplierSerializer(dd_supplier, many=False).data
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='question/(?P<participant_id>\d+)/(?P<dd_question_id>\d+)')
    def dd_participant_question(self, request, category_id, participant_id, dd_question_id):
        question = DueDiligenceQuestion.objects.filter(
            due_diligence_supplier_id=participant_id, due_diligence_supplier__due_diligence__category_id=category_id,
            id=dd_question_id
        ).first()
        dd_supplier = DueDiligenceSupplier.objects.filter(id=participant_id).first()
        context = {
            "question": serializers.DueDiligenceQuestionSerializer(question, many=False).data,
            "participant": serializers.DueDiligenceSupplierSerializer(dd_supplier, many=False).data
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='new/supplier/question/(?P<participant_id>\d+)')
    def create_supplier_question(self, request, category_id, participant_id):
        instance = DueDiligenceQuestion.objects.filter(
            due_diligence_supplier_id=participant_id, due_diligence_supplier__due_diligence__category_id=category_id,
            question=request.data['question']
        ).first()
        if instance:
            s = serializers.DueDiligenceQuestionCreateSerializer(data=request.data, instance=instance)
        else:
            s = serializers.DueDiligenceQuestionCreateSerializer(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['put'], detail=False, url_path='update/supplier/question/(?P<participant_id>\d+)/(?P<dqr_id>\d+)')
    def update_supplier_question(self, request, category_id, participant_id, dqr_id):
        instance = DueDiligenceQuestion.objects.filter(
            due_diligence_supplier_id=participant_id, due_diligence_supplier__due_diligence__category_id=category_id,
            id=dqr_id
        ).first()
        if instance:
            s = serializers.DueDiligenceQuestionCreateSerializer(data=request.data, instance=instance)
            if s.is_valid():
                s.save()
                return Response(s.data, status=status.HTTP_200_OK)
            else:

                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='add/dd/wide/question')
    def create_dd_wide_question(self, request, category_id):
        try:
            for supplier in DueDiligenceSupplier.objects.filter(due_diligence__category_id=category_id):
                data = {
                    "due_diligence_supplier": supplier.id,
                    "question": request.data['question']
                }
                instance = DueDiligenceQuestion.objects.filter(
                    due_diligence_supplier_id=supplier.id,
                    due_diligence_supplier__due_diligence__category_id=category_id,
                    question=request.data['question']
                ).first()
                if instance:
                    s = serializers.DueDiligenceQuestionCreateSerializer(data=data, instance=instance)
                else:
                    s = serializers.DueDiligenceQuestionCreateSerializer(data=data)
                if s.is_valid():
                    s.save()
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# class SupplierView(viewsets.ModelViewSet):
#     def get_queryset(self):
#         # filter by company
#         return apps.apps.get_model('suppliers', 'Supplier').objects.all()
#
#     def get_serializer_class(self):
#         return serializers.SupplierSerializer


class DDQView(viewsets.ModelViewSet):
    def get_queryset(self):
        return DueDiligenceQuestion.objects.filter()

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return


class DDSView(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return


class SupplierSectionScoreView(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return


class PrequalReportView(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return


class AwardLetterView(viewsets.ModelViewSet):
    def get_queryset(self):
        if self.action == "multiple_award_letters":
            return serializers.MultipleAwardLetterSerializer
        return AwardLetter.objects.filter(category_id=self.kwargs['category_id']).order_by('id')

    def get_serializer_class(self):
        return serializers.AwardLetterSerializer

    @action(methods=['post'], detail=False, url_path='create/multiple')
    def multiple_award_letters(self, request, category_id):
        category = Category.objects.filter(id=category_id).first()
        job = category.tender
        company = job.company
        supplier_ids = request.data["supplier_ids"]
        messages = []
        success_letter = ClientDocument.objects.get(
            tender_id=job.id, document_type="success")
        time = datetime.datetime.now()
        
        for supplier_id in supplier_ids:
            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(id=supplier_id).first()

            regret_letter = RegretLetter.objects.filter(
                supplier_id=supplier_id, category_id=category_id).first()
            if not regret_letter:
                file_path = "media/letters/%s/%s/%s/%s" % (
                    company.company_name.replace(" ", "_"),
                    job.title, category.name,
                    supplier.company_name.replace(" ", "_").replace("/", "_"))

                filename = "%s_%d_%d.pdf" % (
                    supplier.company_name.replace(" ", "_").replace("/", "_"),
                    time.year, time.month)
                Path(file_path).mkdir(parents=True, exist_ok=True)
                template_path = "tender/letters/success_letter.html"
                context = {
                    "success_letter": success_letter, "company_name": supplier.company_name,
                    "category": category,
                    "client_company_name": company.company_name,
                    "company": company,
                    "supplier": supplier,
                    "sourcing_activity": "Tender",
                }
                pdf_file_path = weasy_pdf(
                    template_src=template_path, context_dict=context,
                    file_name=filename, file_path=file_path)
                f = open(pdf_file_path, "rb")

                obj, created = AwardLetter.objects.update_or_create(
                    supplier_id=supplier.id, category_id=category_id,
                    defaults={"award_date": datetime.date.today()})
                obj.letter.save(filename, File(f))
                f.close()

                email_subject = f"{company.company_name} TENDER OUTCOME FOR THE {category.name}".upper()
                message = render_to_string(
                    "tender/letters/success_email.html",
                    {"user": supplier, "category": category,
                     "sourcing_activity": "Tender"},
                )
                to_email = supplier.username
                email = EmailMultiAlternatives(email_subject, message, to=[to_email])
                email.attach_alternative(message, "text/html")
                email.attach_file(pdf_file_path)
                email.send()
            else:
                messages.append(f"{supplier.company_name} already has a regret letter")
        context = {
            "response_message": "Success Letters Sent Successfully",
            "messages": messages
        }
        return Response(context, status=status.HTTP_200_OK)


class RegretLetterView(viewsets.ModelViewSet):
    def get_queryset(self):
        return RegretLetter.objects.filter(category_id=self.kwargs['category_id']).order_by('id')

    def get_serializer_class(self):
        if self.action == 'multiple_regret_letters':
            return serializers.MultipleRegretLetterSerializer
        return serializers.RegretLetterSerializer

    @action(methods=['post'], detail=False, url_path='create/multiple')
    def multiple_regret_letters(self, request, category_id):
        category = Category.objects.get(id=category_id)
        job = category.tender
        company = job.company
        supplier_ids = request.data["supplier_ids"]
        messages = []
        regret_letter = get_object_or_404(ClientDocument,
            tender_id=job.id, document_type="regret")
        time = datetime.datetime.now()

        for supplier_id in supplier_ids:
            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(id=supplier_id).first()
            award_letter = AwardLetter.objects.filter(
                supplier_id=supplier_id, category_id=category_id
            ).first()

            if not award_letter:
                file_path = "media/letters/%s/%s/%s/%s" % (
                    company.company_name.replace(" ", "_"),
                    job.title, category.name, supplier.company_name.replace(" ", "_"))

                filename = "%s_%d_%d.pdf" % (
                    supplier.company_name.replace(" ", "_"),
                    time.year,time.month)

                Path(file_path).mkdir(parents=True, exist_ok=True)
                template_path = "tender/letters/regret_letter.html"

                context = {
                    "regret_letter": regret_letter, "company_name": supplier.company_name,
                    "category": category.name, "client_company_name": company.company_name,
                    "supplier": supplier, "sourcing_activity": "Prequalification",
                }
                pdf_file_path = weasy_pdf(
                    template_src=template_path, context_dict=context, file_name=filename,
                    file_path=file_path)
                f = open(pdf_file_path, "rb")
                obj, created = RegretLetter.objects.update_or_create(
                    category_id=category_id, supplier_id=supplier.id,
                    defaults={"regret_date": datetime.date.today()})
                obj.letter.save(filename, File(f))
                f.close()

                email_subject = f"{company.company_name} TENDER OUTCOME FOR THE {category.name}".upper()
                message = render_to_string(
                    "tender/letters/regret_email.html",
                    {"user": supplier, "category": category,},
                )
                to_email = supplier.username
                email = EmailMultiAlternatives(
                    email_subject, message, to=[to_email])
                email.attach_alternative(message, "text/html")
                email.attach_file(pdf_file_path)
                email.send()
            else:
                messages.append(f'{supplier.company_name} already has an award letter')
        context = {
            "response_message": "Regret Letters Sent Successfully",
            "messages": messages
        }
        return Response(context, status=status.HTTP_200_OK)


class CustomLetterView(viewsets.ModelViewSet):
    def get_queryset(self):
        return CustomLetter.objects.filter(category_id=self.kwargs['category_id']).order_by('id')

    def get_serializer_class(self):
        if self.action == 'multiple_custom_letters':
            return serializers.MultipleCustomLetterSerializer
        return serializers.CustomLetterSerializer

    @action(methods=['post'], detail=False, url_path='create/multiple')
    def multiple_custom_letters(self, request, category_id):
        category = Category.objects.get(id=category_id)
        job = category.tender
        company = job.company
        supplier_ids = request.data["supplier_ids"]
        messages = []
        custom_letter = get_object_or_404(ClientDocument,
            tender_id=job.id, document_type="custom")
        time = datetime.datetime.now()

        for supplier_id in supplier_ids:
            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(id=supplier_id).first()

            obj, created = CustomLetter.objects.update_or_create(
                category_id=category_id,supplier_id=supplier.id,
                defaults={
                    "custom_letter_date": datetime.date.today(),
                    # "letter": File(custom_letter.file)
                }
            )
            time = datetime.datetime.now()

            file_path = "media/letters/%s/%s/%s/%s" % (
                company.company_name.replace(" ", "_"),
                job.title, category.name, supplier.company_name.replace(" ", "_"))

            filename = "%s_%d_%d.pdf" % (
                supplier.company_name.replace(" ", "_"), time.year, time.month)
            Path(file_path).mkdir(parents=True, exist_ok=True)
            template_path = "tender/letters/custom_letter.html"

            context = {
                "custom_letter": custom_letter, "company_name": supplier.company_name,
                "category": category.name, "client_company_name": company.company_name,
            }
            pdf_file_path = weasy_pdf(
                template_src=template_path, context_dict=context, file_name=filename, file_path=file_path)
            f = open(pdf_file_path, "rb")
            obj.letter.save(filename, File(f))
            f.close()

            email_subject = custom_letter.subject.upper()
            message = render_to_string(
                "tender/letters/custom_email.html", {"user": supplier, "category": category},
            )
            to_email = supplier.username
            email = EmailMultiAlternatives(email_subject, message, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.attach_file(pdf_file_path)
            email.send()
        context = {
            "response_message": "Letters Sent Successfully",
            "messages": messages
        }
        return Response(context, status=status.HTTP_200_OK)


class DDLetterView(viewsets.ModelViewSet):
    def get_queryset(self):
        return DueDilligenceLetter.objects.filter(category_id=self.kwargs['category_id']).order_by('id')

    def get_serializer_class(self):
        if self.action == 'multiple_dd_letters':
            return serializers.MultipleDDLetterSerializer
        return serializers.DDLetterSerializer

    @action(methods=['post'], detail=False, url_path='create/multiple')
    def multiple_dd_letters(self, request, category_id):
        category = Category.objects.get(id=category_id)
        job = category.tender
        supplier_ids = request.data["supplier_ids"]
        messages = []
        dd_letter = get_object_or_404(ClientDocument,
            tender_id=job.id, document_type="dd")
        dd_letter_path = get_file(dd_letter.file.url)

        for supplier_id in supplier_ids:
            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(id=supplier_id).first()

            obj, created = DueDilligenceLetter.objects.update_or_create(
                category_id=category_id, supplier_id=supplier.id,
                defaults={
                    "due_dilligence_letter_date": datetime.date.today(),
                    # "letter": dd_letter.file
                }
            )

            time = datetime.datetime.now()
            file_path = "media/letters/%s/%s/%s/%s" % (
                job.company.company_name.replace(" ", "_"),
                job.title, category.name,
                supplier.company_name.replace(" ", "_"),
            )
            filename = "%s_%d_%d.pdf" % (
                supplier.company_name.replace(" ", "_"),
                time.year, time.month,
            )
            Path(file_path).mkdir(parents=True, exist_ok=True)
            template_path = "tender/letters/dd_letter.html"
            context = {
                "dd_letter": dd_letter, "company_name": supplier.company_name,
                "category": category.name, "client_company_name": job.company.company_name,
            }
            pdf_file_path = weasy_pdf(
                template_src=template_path, context_dict=context,
                file_name=filename, file_path=file_path,
            )
            f = open(pdf_file_path, "rb")
            obj.letter.save(filename, File(f))
            f.close()

            email_subject = f"{job.company.company_name} TENDER NOTIFICATION FOR DUE DILLIGENCE FOR {category.name}"
            email_subject = email_subject.upper()
            message = render_to_string(
                "tender/letters/dd_email.html",
                {"user": supplier, "category": category, "sourcing_activity": "Prequalification"},
            )
            to_email = supplier.username
            email = EmailMultiAlternatives(email_subject, message, to=[to_email])
            email.attach_alternative(message, "text/html")
            email.attach_file(dd_letter_path)
            email.send()

        context = {
            "response_message": "Letters Sent Successfully",
            "messages": messages
        }
        return Response(context, status=status.HTTP_200_OK)


class ItemView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.ItemCreateUpdateSerializer
        elif self.action == 'retrieve':
            return serializers.ItemDetailSerializer
        return serializers.ItemSerializer

    def get_queryset(self):
        return Item.objects.filter(category_id=self.kwargs['category_id'])


class ClientDocumentView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    def get_queryset(self):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        return ClientDocument.objects.filter(
            tender__company_id=company_id).order_by('id')

    def get_serializer_class(self):
        return serializers.ClientDocumentSerializer

    @action(methods=['post'], detail=False, url_path='update/(?P<job_id>\d+)/(?P<type>[\w\-]+)')
    def job_client_document_update(self, request, job_id, type):
        document = ClientDocument.objects.filter(
            tender_id=job_id, document_type=type).first()
        if document:
            s = serializers.ClientDocumentSerializer(data=request.data, instance=document)
            if s.is_valid():
                s.save()
                return Response(s.data, status=status.HTTP_200_OK)
            else:
                context = {
                    'errors': s.errors,
                    'response_message': 'An error occurred'
                }
                Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "Invalid client document"
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='job/(?P<job_id>\d+)/(?P<type>[\w\-]+)')
    def job_client_document(self, request, job_id, type):
        document = ClientDocument.objects.filter(
            tender_id=job_id, document_type=type).first()
        s = serializers.ClientDocumentSerializer(document, many=False)
        return Response(s.data, status=status.HTTP_200_OK)


class ArchiveView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_queryset(self):
        return Tender.objects.filter(id__in=[])

    def get_serializer_class(self):
        return serializers.JobListSerializer

    @action(methods=['get'], detail=False, url_path='zip/files/(?P<question_id>\d+)')
    def zip_files(self, request, question_id):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        question = Question.objects.filter(
            id=question_id,
            section__category__tender__company_id=company_id).first()
        if question:
            function = ZipQuestionFiles()
            result = function.delay(question_id=question_id)
            context = {
                'task_id': result.task_id
            }
            return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='documents/(?P<category_id>\d+)/supplier/(?P<supplier_id>\d+)')
    def get_archive_documents(self, request, category_id, supplier_id):
        documents = apps.apps.get_model("tender","Question").objects.filter(
                answer_type=apps.apps.get_model("tender","Question").TYPE_UPLOAD, section__category_id=category_id
            )
        other_documents = []

        technical_document = apps.apps.get_model("tender","SupplierPDFResponse").objects.filter(
                category_id=category_id, supplier_id=self.kwargs['supplier_id']
            ).first()
        if technical_document != None:
            technical_document = technical_document.full_document_url
        other_documents.append({"name": "Technical Responses Document", "document_url": technical_document})

        financial_document = apps.apps.get_model("tender","SupplierFinancialResponse").objects.filter(
            category_id=category_id, supplier_id=self.kwargs['supplier_id']
        ).first()
        if financial_document != None:
            financial_document = financial_document.full_document_url

        other_documents.append({"name": "Financial Responses Document", "document_url": financial_document})

        letter = None

        award_letter = apps.apps.get_model("tender","AwardLetter").objects.filter(
            category_id=category_id, supplier_id=self.kwargs['supplier_id']
        ).first()
        if award_letter != None:
            letter = award_letter.full_document_url
        else:
            regret_letter = apps.apps.get_model("tender","RegretLetter").objects.filter(
                category_id=category_id, supplier_id=self.kwargs['supplier_id']
            ).first()
            if regret_letter != None:
                letter = regret_letter.full_document_url
            else:
                custom_letter = apps.apps.get_model("tender","CustomLetter").objects.filter(
                    category_id=category_id, supplier_id=self.kwargs['supplier_id']
                ).first()
                if custom_letter != None:
                    letter = custom_letter.full_document_url
        other_documents.append({"name": "Letter", "document_url": letter})

        duedil_letter = apps.apps.get_model("tender","DueDilligenceLetter").objects.filter(
            category_id=category_id, supplier_id=self.kwargs['supplier_id']
        ).first()
        if duedil_letter != None:
            duedil_letter = duedil_letter.full_document_url
        other_documents.append({"name": "Due Diligence Letter", "document_url": duedil_letter})

        receipt = None
        category_order =apps.apps.get_model("core","CategoryOrder").objects.filter(payment_status=apps.apps.get_model("core","CategoryOrder").PAID, target=ContentType.objects.get_for_model(apps.apps.get_model("tender","Category")),category_id=category_id).first()
        if category_order != None:
            receipt = apps.apps.get_model("core","SupplierReceipt").objects.filter(
            supplier_id=self.kwargs['supplier_id'], reference=category_order.code
            ).first()
            if receipt != None:
                receipt = receipt.full_document_url
        other_documents.append({"name": "Payment Receipt", "document_url": receipt})

        documents = serializers.QuestionArchiveSerializer(documents, many=True, context={'supplier_id': self.kwargs['supplier_id']}).data
        return Response({'documents': documents, 'other_documents': other_documents}, status=status.HTTP_200_OK)


class CategoryReport(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_queryset(self):
        return

    def get_serializer_class(self):
        return

    @action(methods=['get'], detail=False, url_path="financial/ratios")
    def financial_ratios(self, request, category_id):
        report = FinancialRatiosReport()
        result = report.delay(category_id=category_id)
        context = {
            "response_message": "Report generation started",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)


class JobNotificationViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_serializer_class(self):
        return

    @action(methods=['post'], detail=False, url_path="broadcast")
    def broadcast_notifications(self, request, job_id):
        s = serializers.BroadCastNotificationSerializer(data=request.data)
        if s.is_valid():
            result = broadcast_tender_job_notifications.delay(data=request.data)
            context = {
                "task_id": result.task_id
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "An error occured",
            "errors": s.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path="email")
    def email_notifications(self, request, job_id):
        emailed = True
        job = Tender.objects.filter(id=job_id).first()
        s = serializers.EmailNotificationSerializer(data=request.data)
        if s.is_valid():
            if request.data['to'] == "potential":
                data = {
                    "level": request.data["level"], "verb": request.data["verb"], "subject": request.data["subject"],
                    "message": request.data["content"], "potential_selection": request.data["potential_selection"],
                    "type": request.data["to"], "emailed": emailed, "model_content_type": "prequalification",
                    "company_id": job.company_id
                }

                emails = SendTenderEmailNotifications()
                result = emails.delay(job_id=job_id, data=data)
                context = {
                    "task_id": result.task_id,
                    "response_message": "Email notifications initiated successfully!"
                }
                return Response(context, status=status.HTTP_200_OK)
            elif request.data['to'] == "all":
                pass
            elif request.data['to'] == "paid":
                pass
        context = {
            "response_message": "An error occured",
            "errors": s.errors
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False, url_path="email/invite")
    def invite_notifications(self, request, job_id):
        result = send_tender_job_invite_email.delay(job_id=job_id)
        context = {
            "response_message": "Invite emails initiated successfully",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="sms/invite")
    def sms_notifications(self, request, job_id):
        result = send_tender_job_invite_sms.delay(job_id=job_id)
        context = {
            "response_messsage": "SMS invite notification initiated successfully",
            "task_id": result.task_id
        }
        return Response(context, status=status.HTTP_200_OK)


class SupplierAdvancedTenderView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)

    def get_serializer_class(self):
        return serializers.TenderAdvancedSupplierResponseSerializer
    
    def get_queryset(self):
        supplier_tender_responses = SupplierFinancialResponse.objects.filter(
            category_id=self.kwargs["category_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return supplier_tender_responses

    def create(self, request, *args, **kwargs):
        supplier_id = kwargs["supplier_id"]
        category_id = kwargs["category_id"]
        price_template = request.FILES["excel_url"]
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        supplier = apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
        category = Category.objects.filter(id=category_id).first()

        if supplier is not None and category is not None:
            sup_response,created = SupplierFinancialResponse.objects.update_or_create(
                supplier_id=supplier_id, category_id=category_id,defaults={"excel_url":price_template}
            )
            if sup_response:
                suplier_res = submit_tender_rfq.delay(sup_response.category_id, sup_response.supplier_id, sup_response.excel_url.url)
                s_context = {"task_id": suplier_res.task_id}
                res = AsyncResult(s_context["task_id"])
                task_result = res.get()
                if task_result["result"]== "success":
                    if created:
                        tender_send_participation_acknowledgment.delay(
                            supplier_id=supplier_id, category_id=category_id, created=True
                        )
                    else:
                        tender_send_participation_acknowledgment.delay(
                            supplier_id=supplier_id, category_id=category_id
                        )
                    context = {
                        "response_message": task_result["response_message"],
                        "task_id": s_context["task_id"],
                    }
                    return Response(context, status=status.HTTP_200_OK)
                elif task_result["result"] == "error":
                    return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplierFinancialTotalView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return serializers.SupplierFinancialTotalSerializer

    def get_queryset(self):
        supplier_tender_totals = SupplierFinancialTotal.objects.filter(
            category_id=self.kwargs["category_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return supplier_tender_totals.order_by("id")

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            supplier = data["supplier"]
            category = data["category"]

            tender_total, created = SupplierFinancialTotal.objects.update_or_create(
                supplier_id=supplier,
                category_id=category,
                defaults={
                    "score": data["score"],
                    "has_outlier": False,
                    "has_blank": False,
                },
            )
            if created:
                tender_send_participation_acknowledgment.delay(
                    supplier_id=supplier, category_id=category, created=True
                )
            else:
                tender_send_participation_acknowledgment.delay(
                    supplier_id=supplier, category_id=category
                )

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            error = {"error": str(e)}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
