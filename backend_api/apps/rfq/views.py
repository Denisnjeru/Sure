from crypt import methods
from dis import Instruction
from enum import unique
from os import stat
from unicodedata import category
from wsgiref import headers
from django.shortcuts import render
from requests import post
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser,FileUploadParser
from celery.result import AsyncResult
from yaml import serialize

from apps import rfq

from apps.rfq import serializers
from apps.rfq.emails import (
    send_financial_responses,
    send_participation_acknowledgment,
    send_rfq_category_emails,
)
from apps.rfq.models import *
from apps.prequal import serializers as prequal_serializers
from apps.rfq.reports import (
    RFQFinancialReport,
    RFQSummaryReport,
    rfq_job_summary_report,
    rfq_participation_status,
)
from apps.rfq.tasks import download_current_prices_import, import_current_supplier_prices, invite_suppliers_rfq, \
    submit_rfq, import_category_suppliers
from apps.suppliers.models import Supplier


class JobView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    def get_serializer_class(self):
        if self.action == "list" or self.action == "retrieve":
            return serializers.JobListSerializer
        else:
            return serializers.JobCreateUpdateSerializer

    def get_queryset(self):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        return Rfq.objects.filter(company_id=company_id)

    def get_queryset(self):
        if "company_id" in self.request.auth.payload:
            return Rfq.objects.filter(company_id=self.request.auth.payload["company_id"])
        return Rfq.objects.all()

    def create(self, request, *args, **kwargs):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        data_copy = request.data.copy()
        data_copy["company"] = company_id
        data_copy["created_by"] = request.user.id
        serializer = self.get_serializer(data=data_copy)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance.title = request.data['title']
        instance.unique_reference =request.data['unique_reference']
        instance.save()
        res_serializer = self.get_serializer(instance)
        return Response(
            res_serializer.data,status=status.HTTP_201_CREATED   
        )
       
    @action(
        methods=["get"],
        detail=False,
        url_path="generate/job/summary/report/(?P<rfq_id>\d+)",
    )
    def generate_job_summary_report(self, request, rfq_id, *args, **kwargs):
        rfq = Rfq.objects.filter(id=rfq_id).first()
        if rfq is not None:
            job_report = RFQJobReport.objects.filter(job=rfq).first()
            if job_report is not None:
                response_url = job_report.job_savings.url
                response_url = response_url.split("/")[1:]
                response_url = ("/").join(response_url)
                context = {"report": response_url}
                return Response(context, status.HTTP_200_OK)
            else:
                report = RFQSummaryReport()
                result = report.delay(rfq_id=rfq_id)
                context = {
                    "response_message": "Job summary report generation in progress",
                    "task_id": result.task_id,
                }
                return Response(status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="generate/job/participation_status/report/(?P<rfq_id>\d+)")
    def generate_job_participation_status_report(self, request, rfq_id, *args, **kwargs):
        report = rfq_participation_status
        result = report.delay(rfq_id=rfq_id, *args, **kwargs)
        context = {
            "response_message": "Job participation status report generation in progress",
            "task_id": result.task_id,
        }
        return Response(context)

    @action(methods=["get"], detail=False, url_path=("defaults"))
    def defaults(self, request, *args, **kwargs):
        category_types = (
            apps.get_model("core", "CategoryType").objects.order_by("id").all()
        )
        currencies = apps.get_model("core", "Currency").objects.order_by("id").all()
        d = serializers.RfqCategoryTypeSerializer(category_types, many=True)
        s = serializers.CurrencySerializer(currencies, many=True)
        context = {
            "category_types": d.data,
            "currencies": s.data,
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path=("approve_job/(?P<rfq_id>\d+)"))
    def approve_job(self, request, rfq_id, *args, **kwargs):
        rfq = Rfq.objects.filter(id=rfq_id).first()
        if rfq is not None:
            rfq.status = "final"
            rfq.approved_by_id = request.user.id
            rfq.save()
            context = {"message": "Job approved succesfully"}
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {"message": "Job does not exist"}
            return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['post'], detail=False, url_path='upload/category/suppliers/(?P<rfq_id>\d+)')
    def upload_category_suppliers(self, request, rfq_id):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        instance = Rfq.objects.filter(
            company_id=company_id, id=rfq_id
        ).first()
        s = serializers.RFQCatSupplierSerializer(data=request.data, instance=instance)

        if s.is_valid():
            s.save()
            result = import_category_suppliers.delay(job_id=int(rfq_id))
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


class RfqCategoryView(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated)
    parser_classes = (MultiPartParser, FormParser, JSONParser,FileUploadParser,)
   

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Category.objects.none()
        return Category.objects.filter(rfq_id=self.kwargs["job_id"]).order_by("id")

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.RfqCategoryCreateSerializer
        if self.action == "retrieve":
            return serializers.RfqCategoryRetrieveSerializer
        if self.action == "upload_current_prices_template":
            return serializers.RFQExcelUploadSerializer
        return serializers.RfqCategorySerializer

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            data["rfq"] = kwargs["job_id"]

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            vat_rate = None
            if request.data["vat_rate"] != "" and request.data["vat_rate"] != " ":
                vat_rate = int(request.data["vat_rate"])
            rfq_category = Category.objects.create(
                rfq_id=request.data["rfq"],
                name=request.data["name"],
                opening_date=request.data["opening_date"],
                closing_date=request.data["closing_date"],
                unique_reference=request.data["unique_reference"],
                category_type_id=request.data["category_type"],
                instructions=request.data["instructions"],
                items_template=request.data["items_template"],
                currency_id=request.data["currency"],
                rfq_type=request.data["rfq_type"],
                vatable=request.data["vatable"],
                vat_rate=vat_rate
            )
            rfq_category.save()

            res_serializer = serializers.RfqCategorySerializer(rfq_category)
            headers = self.get_success_headers(res_serializer.data)

            return Response(
                res_serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            error = {"error": str(e)}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        pass

    @action(methods=["get"], detail=False, url_path="participants/(?P<category_id>\d+)")
    def participants(self, request, category_id, **kwargs):
        suppliers = []
        rfq_scores = SupplierRfqTotal.objects.filter(category_id=category_id)
        if rfq_scores.count() == 0:
            responses = RFQItemResponse.objects.filter(
                rfq_item__category_id=category_id
            )
            for response in responses:
                supplier = response.supplier
                if supplier not in suppliers:
                    suppliers.append(supplier)
            partcipants = set(suppliers)
        else:
            partcipants = Supplier.objects.filter(
                id__in=rfq_scores.only("supplier_id").values("supplier_id")
            )

        response_serializer = serializers.ParticipantSerializer(partcipants, many=True)
        return Response(response_serializer.data)

    @action(
        methods=["post"], detail=False, url_path="invite_suppliers/(?P<category_id>\d+)"
    )
    def invite_suppliers(self, request, category_id, *args, **kwargs):
        data = request.data
        supplier_emails = data["emails"].split(",")

        for supplier_email in supplier_emails:
            try:
                if (
                    RfqInvitee.objects.filter(
                        category_id=category_id, email=supplier_email
                    ).count()
                    < 1
                ):
                    supplier = (
                        apps.get_model("suppliers", "Supplier")
                        .objects.filter(email=supplier_email.replace(" ", ""))
                        .first()
                    )

                    if supplier is not None:
                        RfqInvitee.objects.update_or_create(
                            category_id=category_id,
                            supplier=supplier,
                            email=supplier_email,
                        )
                    else:
                        RfqInvitee.objects.update_or_create(
                            category_id=category_id,
                            email=supplier_email,
                        )
            except Exception as e:
                error = {"error": str(e)}

        # invite_suppliers_rfq.delay(category_id)
        invite_suppliers_rfq(category_id)

        context = {"response_message": "Suppliers invite emails sent successfully"}
        return Response(context, status=status.HTTP_201_CREATED)

    @action(
        methods=["get"], detail=False, url_path="invited/suppliers/(?P<category_id>\d+)"
    )
    def invited_suppliers(self, request, **kwargs):
        invitees = RfqInvitee.objects.filter(category_id=kwargs["category_id"])
        s = serializers.InvitedSupplierSerializer(invitees, many=True)
        return Response(s.data)

    @action(methods=["get"], detail=False, url_path="close/(?P<category_id>\d+)")
    def close_rfq(self, request, job_id, category_id):
        rfq_category = Category.objects.filter(id=category_id).first()

        if rfq_category is not None:
            if rfq_category.status_open:
                try:
                    rfq_category.status_open = False
                    rfq_category.closing_date = timezone_aware_time()
                    rfq_category.save()
                    if rfq_category.participants["count"] > 0:
                        send_financial_responses.delay(category_id)

                    # generate financial report
                    report = RFQFinancialReport()
                    result = report.delay(category_id=category_id)
                    # remember run asynchronously
                    # rfq_job_summary_report(category_id)
                    context = {"message": "RFQ category closed successfuly"}
                    return Response(context, status=status.HTTP_201_CREATED)
                except Exception as e:
                    context = {"message": str(e)}
                    return Response(context, status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                context = {"message": "RFQ category already closed"}
                return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(methods=["post"], detail=False, url_path="open/(?P<category_id>\d+)")
    def open_rfq(self, request, job_id, category_id):
        data_copy = request.data.copy()
        data_copy["id"] = category_id
        serializer = serializers.RfqOpenSerializer(data=data_copy)

        rfq_category = Category.objects.filter(id=data_copy["id"]).first()

        if rfq_category is not None:
            if serializer.is_valid():
                serializer.save()
                context = {
                    "message": "Category opened successfully",
                    "data": serializer.data,
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {"message": "Invalid data"}
                return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {"message": "Category is open"}
            return Response(context, status.HTTP_400_BAD_REQUEST)

    @action(
        methods=["get"], detail=False, url_path="related/prequals/(?P<category_id>\d+)"
    )
    def related_prequals(self, request, category_id):
        rfq = Category.objects.filter(id=category_id).first()
        related_prequals = apps.apps.get_model("prequal", "Category").filter(
            category_type=rfq.category_type
        )
        response_serializer = prequal_serializers.CategoryListSerializer(
            related_prequals, many=True
        )
        return Response(response_serializer.data)

    @action(
        methods=["get"],
        detail=False,
        url_path="generate/supplier/rfq/report/pdf/(?P<category_id>\d+)/(?P<supplier_id>\d+)",
    )
    def supplier_rfq_report_pdf(self, request, category_id, supplier_id, **kwargs):
        category = Category.objects.filter(id=category_id).first()
        supplier = (
            apps.get_model("suppliers", "Supplier")
            .objects.filter(id=supplier_id)
            .first()
        )
        if category is not None and supplier is not None:
            sup_response = SupplierResponse.objects.filter(
                supplier=supplier, category=category
            ).first()
            if sup_response is not None:
                response_url = sup_response.document_url.url
                response_url = response_url.split("/")[1:]
                response_url = ("/").join(response_url)
                context = {"report": response_url}
                return Response(context, status.HTTP_200_OK)
            else:
                return Response(status.HTTP_204_NO_CONTENT)
        else:
            return Response(status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        url_path="generate/category/rfq/report/pdf/(?P<category_id>\d+)",
    )
    def category_rfq_report_pdf(self, request, category_id, **kwargs):
        category = Category.objects.filter(id=category_id).first()
        if category is not None:
            report = RFQCategoryReport.objects.filter(category=category).first()
            if report is not None:
                response_url = report.category_rfq_pdf.url
                response_url = response_url.split("/")[1:]
                response_url = ("/").join(response_url)
                context = {"report": response_url}
                return Response(context, status.HTTP_200_OK)
            else:
                report = rfq_job_summary_report(category_id)
                response_url = report.category_rfq_pdf.url
                response_url = response_url.split("/")[1:]
                response_url = ("/").join(response_url)
                context = {"report": response_url}
                return Response(context, status.HTTP_200_OK)
        else:
            return Response(status.HTTP_204_NO_CONTENT)

    @action(
        methods=["get"],
        detail=False,
        url_path="generate/financial/report/(?P<category_id>\d+)",
    )
    def generate_financial_report(self, request, category_id, *args, **kwargs):
        category = Category.objects.filter(id=category_id).first()
        if category is not None:
            report = RFQCategoryReport.objects.filter(category=category).first()
            if report is not None:
                response_url = report.financial.url
                response_url = response_url.split("/")[1:]
                response_url = ("/").join(response_url)
                context = {"report": response_url}
                return Response(context, status.HTTP_200_OK)
            else:
                report = RFQFinancialReport()
                result = report.delay(category_id=category_id)
                context = {
                    "response_message": "Financial report generation in progress",
                    "task_id": result.task_id,
                }
                return Response(context)
        else:
            return Response(status.HTTP_204_NO_CONTENT)

    @action(methods=["get"], detail=False, url_path="refresh/scores/(?P<rfq_id>\d+)")
    def refresh_rfq_scores(self, request, rfq_id):
        if self.request.query_params.get('company_id'):
            company_id = int(self.request.query_params.get('company_id'))  
        else:
            company_id = self.request.auth.payload['company_id']

        rfq = Rfq.objects.filter(
            id=rfq_id, company_id=company_id
        ).first()
        if rfq is not None:
            rfq.refresh_scores()
        s = serializers.RfqCategoryRetrieveSerializer(rfq, many=False)
        return Response(s.data)

    @action(
        methods=["post"],
        detail=False,
        url_path="emails/notification_emails/(?P<category_id>\d+)/(?P<type>[\w\-]+)",
    )
    def send_rfq_category_emails(
        self, request, category_id, type=None, *args, **kwargs
    ):
        rfq = Category.objects.filter(id=category_id).first()
        if rfq is not None:
            if type == "reminder":
                send_rfq_category_emails(category_id=category_id, type="reminder")
            elif type == "extension":
                send_rfq_category_emails(category_id=category_id, type="extension")
            context = {
                "response_message": "Emails sent successfuly",
            }
            return Response(context)

        else:
            context = {
                "error": "Emails not sent",
            }
            return Response(context)

    @action(
        methods=["get"],
        detail=False,
        url_path="download/current_prices/template/(?P<category_id>\d+)",
    )
    def download_current_prices_template(self, request, category_id, *args, **kwargs):
        rfq_category = Category.objects.filter(id=category_id).first()
        if rfq_category is not None:
            file_download = download_current_prices_import.delay(
                category_id=rfq_category.id
            )
            file_context = {"task_id": file_download.task_id}
            res = AsyncResult(file_context["task_id"])
            task_result = res.get()
            if task_result["result"] == "success":
                context = {
                    "response_message": task_result["response_message"],
                    "filepath": task_result["filepath"],
                    "task_id": file_context["task_id"],
                }
                return Response(context, status=status.HTTP_200_OK)
            elif task_result["result"] == "error":
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='upload/current_prices/template/(?P<category_id>\d+)')
    def upload_current_prices_template(self, request, category_id, *args, **kwargs):
        rfq_category = Category.objects.filter(id=category_id).first()
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        
        if serializer.is_valid():
            file_obj = request.FILES["price_import_file"]
            rfq_category.current_prices_template = file_obj
            rfq_category.save()

            file_url = rfq_category.current_prices_template.url
            print(file_url)
            file_upload = import_current_supplier_prices.delay(file_url)
            file_context = {"task_id": file_upload.task_id}
            res = AsyncResult(file_context["task_id"])
            task_result = res.get()
            if task_result["result"]== "success":
                context = {
                    "response_message": task_result["response_message"],
                    "task_id": file_context["task_id"],
                }
                return Response(context, status=status.HTTP_200_OK)
            elif task_result["result"] == "error":
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            context = {
                "response_message": "Error uploading template"
            }
            return Response(context,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ItemView(viewsets.ModelViewSet):
    # permission_classes = IsAuthenticated

    def get_serializer_class(self):
        if self.action == "create":
            return serializers.RfqItemCreateUpdateSerializer
        if self.action == "retrieve":
            return serializers.RfqItemRetrieveSerializer
        return serializers.RfqItemSerializer

    def get_queryset(self):
        items = RFQItem.objects.filter(
            category_id=self.kwargs["category_id"],
        )
        return items.order_by("item_number")

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = request.data
            data["rfq"] = kwargs["rfq_id"]
            self.perform_create(serializer=serializer)
            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            error = {"error": str(e)}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplierItemResponseView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return serializers.RfqItemResponseSerializer

    def get_queryset(self):
        item_responses = RFQItemResponse.objects.filter(
            rfq_item_id=self.kwargs["item_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return item_responses.order_by("id")

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data["rfq_item"] = int(kwargs["item_id"])
            data["supplier"] = kwargs["supplier_id"]

            rfq_item_response = RFQItemResponse.objects.update_or_create(
                supplier_id=data["supplier"],
                item_number=data["item_number"],
                rfq_item_id=data["rfq_item"],
                defaults={
                    "unit_price": data["unit_price"],
                    "total_price": data["total_price"],
                },
            )

            headers = self.get_success_headers(serializer.data)

            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )
        except Exception as e:
            error = {"error": str(e)}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SupplierCategoryResponseView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return serializers.RfqSupplierResponseSerializer

    def get_queryset(self):
        supplier_responses = SupplierResponse.objects.filter(
            supplier_id=self.kwargs["supplier_id"],
            category_id=self.kwargs["category_id"],
        ).order_by("id")
        return supplier_responses


class SupplierRfqTotalView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return serializers.SupplierRFQTotalSerializer

    def get_queryset(self):
        supplier_rfq_totals = SupplierRfqTotal.objects.filter(
            category_id=self.kwargs["category_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return supplier_rfq_totals.order_by("id")

    def create(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            supplier = data["supplier"]
            category = data["category"]

            rfq_total, created = SupplierRfqTotal.objects.update_or_create(
                supplier_id=supplier,
                category_id=category,
                defaults={
                    "score": data["score"],
                    "has_outlier": False,
                    "has_blank": False,
                },
            )
            if created:
                send_participation_acknowledgment.delay(
                    supplier_id=supplier, category_id=category, created=True
                )
            else:
                send_participation_acknowledgment.delay(
                    supplier_id=supplier, category_id=category
                )

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            error = {"error": str(e)}
            return Response(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupplierAdvancedRFQView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)

    def get_serializer_class(self):
        return serializers.RfqAdvancedSupplierResponseSerializer
    
    def get_queryset(self):
        supplier_rfq_responses = SupplierResponse.objects.filter(
            category_id=self.kwargs["category_id"],
            supplier_id=self.kwargs["supplier_id"],
        )
        return supplier_rfq_responses

    def create(self, request, *args, **kwargs):
        supplier_id = kwargs["supplier_id"]
        category_id = kwargs["category_id"]
        price_template = request.FILES["document_url"]
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        supplier = apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
        category = Category.objects.filter(id=category_id).first()

       
        if supplier is not None and category is not None:
            sup_response,created = SupplierResponse.objects.update_or_create(
                supplier_id=supplier_id, category_id=category_id,defaults={"document_url":price_template}
            )
            if sup_response:
                suplier_res = submit_rfq.delay(sup_response.category_id, sup_response.supplier_id, sup_response.document_url.url)
                s_context = {"task_id": suplier_res.task_id}
                res = AsyncResult(s_context["task_id"])
                task_result = res.get()
                if task_result["result"]== "success":
                    if created:
                        send_participation_acknowledgment.delay(
                            supplier_id=supplier_id, category_id=category_id, created=True
                        )
                    else:
                        send_participation_acknowledgment.delay(
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

class ArchiveView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]
    
    def get_queryset(self):
        return []

    def get_serializer_class(self):
        return serializers.JobListSerializer

    @action(methods=['get'], detail=False, url_path='documents/(?P<category_id>\d+)/supplier/(?P<supplier_id>\d+)')
    def get_archive_documents(self, request, category_id, supplier_id):
        documents = []
        other_documents = []

        financial_document = apps.apps.get_model("rfq","SupplierResponse").objects.filter(
            category_id=category_id, supplier_id=self.request.auth.payload['user_id']
        ).first()
        if financial_document != None:
            financial_document = financial_document.full_document_url

        other_documents.append({"name": "Financial Responses Document", "document_url": financial_document})

        return Response({'documents': documents, 'other_documents': other_documents}, status=status.HTTP_200_OK)