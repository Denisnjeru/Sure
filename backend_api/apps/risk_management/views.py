from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from uritemplate import partial
from .models import (
    RiskManagement, Category, RiskReport, Section, Question, SupplierResponse, MarkingScheme,
    QualityAssurance, QualityAssuranceQuestion, QualityAssuranceResponse, SupplierSectionScore, JobSupportingDocuments, CategorySupportingDocuments
)
from rest_framework.parsers import FileUploadParser, JSONParser, MultiPartParser, FormParser
from .serializers import (
    RiskCategoryRetrieveSerializer, RiskListSerializer, RiskRetrieveSerializer, RiskCreateUpdateSerializer, RiskCategoryListSerializer, RiskCategoryCreateUpdateSerializer,
    RiskSectionListSerializer, RiskSectionCreateUpdateSerializer, RiskQuestionListSerializer, RiskQuestionCreateUpdateSerializer,
    RiskMarkingSchemeSerializer, RiskSRSerializer, RiskQASerializer, RiskQAQSerializer, RiskQARSerializer, RiskJobSupportingDocumentsSerializer, RiskApproveSerializer, RiskCategorySupportingDocumentsSerializer, 
    RiskSectionRetrieveSerializer, RiskQuestionRetrieveSerializer, RiskQAInstructionSerializer
)
from ..buyer.models import Buyer
from apps.risk_management import serializers


class JobView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return RiskListSerializer
        if self.action == 'retrieve':
            return RiskRetrieveSerializer
        if self.action == 'approve_job':
            return 
        else:
            return RiskCreateUpdateSerializer

    def get_queryset(self):
        return RiskManagement.objects.filter(company_id=self.request.auth['company_id'])

    def create(self, request, *args, **kwargs):
        
        #Add created_by and Company_id
        data = request.data
        data['created_by'] = request.user.id
        data['company'] = request.auth.payload['company_id']

        print(data)
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(methods=['post'], detail=False, url_path='approve/(?P<job_id>\d+)')
    def approve_job(self, request, job_id):
        try:
            RiskManagement.objects.filter(id=job_id).update(approved_by=request.user.id)
            return Response('Approved', status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryView(viewsets.ModelViewSet):
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    def get_queryset(self):
        return Category.objects.filter(riskmanagement_id=self.kwargs['job_id'])


    def get_serializer_class(self):
        if self.action == 'list':
            return RiskCategoryListSerializer
        if self.action == 'retrieve':
            return RiskCategoryRetrieveSerializer
        else:
            return RiskCategoryCreateUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            #Add risk management id
            data = request.data
            data['riskmanagement'] = kwargs['job_id']

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SectionView(viewsets.ModelViewSet):
    
    def get_queryset(self):
        return Section.objects.filter(category_id=self.kwargs['category_id'])

    def get_serializer_class(self):
        if self.action == 'list':
            return RiskSectionListSerializer
        if self.action == 'retrieve':
            return RiskSectionRetrieveSerializer
        else:
            return RiskSectionCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        try:
            #Add risk management id
            data = request.data
            data['category'] = kwargs['category_id']

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class QuestionView(viewsets.ModelViewSet):
    def get_queryset(self):
        return Question.objects.filter(section_id=self.kwargs['section_id'])

    def get_serializer_class(self):
        if self.action == 'list':
            return RiskQuestionListSerializer
        if self.action == 'retrieve':
            return RiskQuestionRetrieveSerializer
        else:
            return RiskQuestionCreateUpdateSerializer
    
    def create(self, request, *args, **kwargs):
        try:
            #Add risk management id
            data = request.data
            data['section'] = kwargs['section_id']

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)



class MarkingSchemeView(viewsets.ModelViewSet):
    def get_queryset(self):
        return MarkingScheme.objects.filter(question_id=self.kwargs['question_id'])

    def get_serializer_class(self):
        return RiskMarkingSchemeSerializer


class SupplierResponseView(viewsets.ModelViewSet):
    def get_queryset(self):
        supplier_response = SupplierResponse.objects.filter(
            question_id=self.kwargs['question_id'], supplier_id=self.kwargs['supplier_id']
        )
        return supplier_response

    def get_serializer_class(self):
        return RiskSRSerializer


class QAView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        if self.create == 'create':
            return RiskQASerializer
        if self.action == 'get_qa_sections':
            return RiskQAInstructionSerializer
        if self.action == 'retrieve':
            return RiskQAInstructionSerializer
        else:
            return RiskQASerializer

    def get_queryset(self):
        return QualityAssurance.objects.filter(category_id=self.kwargs['category_id'])
    
    def create(self, request, *args, **kwargs):
        try:
            #Add risk management id
            data = request.data
            data['category'] = kwargs['category_id']

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @action(methods=['get'], detail=False, url_path='get_qa_sections')
    def get_qa_sections(self, request, category_id):
        try:
            qs = QualityAssurance.objects.filter(category_id=self.kwargs['category_id']).first()
            print(qs)
            serializer = self.get_serializer(instance=qs)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class QAQView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        return RiskQAQSerializer
    
    def get_queryset(self):
        return QualityAssuranceQuestion.objects.filter(quality_assurance_id=self.kwargs['qa_id'])
    
    def create(self, request, *args, **kwargs):
        try:
            #Add risk management id
            data = request.data
            data['quality_assurance'] = kwargs['qa_id']

            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['post'], detail=False, url_path='create_qa_questions')
    def create_qa_questions(self, request, qa_id):
        try:
            ins = QualityAssurance.objects.filter(id=self.kwargs['qa_id']).first()

            # List of questions and instructions
            qaquestions = request.data
            for qaquestion in qaquestions:
                ins_q = QualityAssurance.objects.filter(id=qaquestion['question']).first()
                obj, created = QualityAssuranceQuestion.objects.update_or_create(
                    question_id = qaquestion['question'],
                    quality_assurance_id = self.kwargs['qa_id'],
                    defaults={'quality_assurance_id': self.kwargs['qa_id'], 'question_id': qaquestion['question'],
                            'verification_instruction': qaquestion['verification_instruction']
                    }
                )
            return Response('created successfully', status=status.HTTP_201_CREATED)
        except Exception as e:
            error = {'error': str(e)}
            print(error)
            return Response(error, status= status.HTTP_500_INTERNAL_SERVER_ERROR)

class QARView(viewsets.ModelViewSet):
    
    def get_serializer_class(self):
        return RiskQARSerializer

    def get_queryset(self):
        return QualityAssuranceResponse.objects.filter(quality_assurance_question_id=self.kwargs['qa_question_id'])

class SupplierSectionScoreView(viewsets.ModelViewSet):
    def get_queryset(self):
        return SupplierSectionScore.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return


class RiskReportView(viewsets.ModelViewSet):
    def get_queryset(self):
        return RiskReport.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return
        return    

class RiskSupportingDocumentView(viewsets.ModelViewSet):

    def get_serializer_class(self):
        return RiskJobSupportingDocumentsSerializer

    def get_queryset(self):
        return JobSupportingDocuments.objects.filter(riskmanagement_id=self.kwargs['job_id'])

class RiskCategorySupportingDocumentView(viewsets.ModelViewSet):

    def get_serializer_class(self):
        return RiskCategorySupportingDocumentsSerializer

    def get_queryset(self):
        return CategorySupportingDocuments.objects.filter(category_id=self.kwargs['job_id'])
