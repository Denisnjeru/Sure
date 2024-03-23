from django.shortcuts import render
from django.db.models import Case, When

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_403_FORBIDDEN
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser

from apps.authentication.models import User
from apps.core.models import Job
from apps.suppliers.models import Supplier
from apps.buyer.models import Buyer
from apps.contract.models import *

from .serializers import (
    SupplierContractSerializer, ContractSectionSerializer, ContractDocumentSerializer, CategorySupplierSerializer, ContractSectionListSerializer,
    ContractSectionSerializer, SupplierContractListSerializer, SupplierContractRetrieveSerializer, ContractTemplateSerializer,
    ContractTemplateListSerializer, ContractSerializer, ContractCreateSerializer, ContractRetrieveSerializer, ContractSectionsCombineSerializer,
    SupplierContractSaveSerializer, SupplierContractRevisionsSerializer, ContractRevisionsSerializer, ContractUpdateSerializer)
from apps.core.serializers import JobsSerializer
from apps.suppliers.serializers import SupplierListSerializer

from apps.contract.utils import contract_update_request_email, contract_revision_changes


class JobsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_serializer_class(self):
        return JobsSerializer

    def get_queryset(self):
        return Job.objects.all()

    @action(methods=['get'], detail=False, url_path='(?P<company_id>\d+)')
    def jobs_list(self, request, company_id):
        queryset = Job.objects.filter(company_id=company_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

class CategorySupplierView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_serializer_class(self):
        return SupplierListSerializer

    def get_queryset(self):
        suppliers = CategorySupplier.objects.filter(category_id=self.kwargs['category_id']).values_list('supplier', flat=True)
        return Supplier.objects.filter(id__in=suppliers)

    @action(methods=['get'], detail=False, url_path='(?P<category_id>\d+)/suppliers')
    def suppliers_list(self, request, category_id):
        page = self.paginate_queryset(self.get_queryset())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

class SupplierContractView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierContractListSerializer
        elif self.action == 'retrieve':
            return SupplierContractRetrieveSerializer
        elif self.action == 'live_edit':
            return SupplierContractRetrieveSerializer
        elif self.action == 'live_edit_save':
            return SupplierContractSaveSerializer
        elif self.action == 'category_contracts':
            return SupplierContractListSerializer
        else:
            return SupplierContractSerializer

    def get_queryset(self):
        return SupplierContract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_by = Buyer.objects.get(username=request.user.username)
        instance = SupplierContract.objects.create(
            supplier_id=request.data['supplier'],
            category_id=request.data['category'],
            contact_emails=request.data['contact_emails'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            created_by=created_by
        )

        contract_content = ''
        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(request.data['source_list'])])

        if request.data['source'] == 'sections':
            selectedSections = ContractSection.objects.filter(id__in=request.data['source_list']).order_by(preserved)
            for selectedSection in selectedSections:
                contract_content += selectedSection.content

        if request.data['source'] == 'templates':
            selectedTemplate = ContractTemplate.objects.filter(id__in=request.data['source_list']).first()
            contract_content += selectedTemplate.content

        instance.content = contract_content
        instance.save()

        return_serializer = SupplierContractSerializer(instance)
        return Response(
            return_serializer.data, status=HTTP_201_CREATED
        )

    @action(methods=['get'], detail=False, url_path='category/(?P<category_id>\d+)')
    def category_contracts(self, request, category_id):
        queryset = SupplierContract.objects.filter(category_id=category_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='(?P<contract_id>\d+)/live_edit_save')
    def live_edit_save(self, request, contract_id):
        contract = SupplierContract.objects.filter(id=contract_id).first()

        if request.data['type'] == 'auto':
            contract.live_edit = True
            contract.save()

            revision = SupplierContractRevisions.objects.get(
                contract_id = contract.id,
                editor_id = request.user.id,
                live_edit = True
            )

            revision.content = request.data['content']
            revision.save()

        if request.data['type'] == 'save':
            contract.live_edit = False
            contract.live_editor = None
            contract.content = request.data['content']
            contract.save()

            revision = SupplierContractRevisions.objects.get(
                contract_id = contract.id,
                editor_id = request.user.id,
                live_edit = True
            )

            revision.live_edit = False
            revision.content = request.data['content']
            revision.save()

        serializer = SupplierContractRetrieveSerializer(contract)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='(?P<contract_id>\d+)/live_edit')
    def live_edit(self, request, contract_id):
        contract = SupplierContract.objects.filter(id=contract_id).first()

        if contract.live_edit == False:
            contract.live_editor_id = request.user.id
            contract.live_edit = True
            contract.save()

            revision = SupplierContractRevisions.objects.create(
                contract_id = contract.id,
                editor_id = request.user.id,
                content = contract.content,
                live_edit = True
            )

        serializer = self.get_serializer(contract)

        return Response(serializer.data, status=HTTP_200_OK)

class ContractView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser)

    def get_serializer_class(self):
        if self.action == 'create':
            return ContractCreateSerializer
        elif self.action == 'update':
            return ContractUpdateSerializer
        elif self.action == 'retrieve':
            return ContractRetrieveSerializer
        elif self.action == 'contract_revisions':
            return ContractRevisionsSerializer
        elif self.action == 'contract_revision':
            return ContractRevisionsSerializer

        return ContractSerializer

    def get_queryset(self):
        return Contract.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        created_by = User.objects.get(username=request.user.username)
        contract_with=ContentType.objects.filter(model=request.data['contract_with']).first()
        contract_for=ContentType.objects.filter(model=request.data['contract_for']).first()

        instance = Contract.objects.create(
            contract_with=contract_with,
            entity_id=request.data['entity_id'],
            contract_for=contract_for,
            target_id=request.data['target_id'],
            contact_emails=request.data['contact_emails'],
            start_date=request.data['start_date'],
            end_date=request.data['end_date'],
            created_by=created_by
        )

        document = None
        try:
            document = request.data['document']
        except Exception as e:
            pass

        if document is not None:
            instance.document = document
            instance.save()

        if request.data['source'] == 'sections':
            preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(request.data['source_list'])])
            selectedSections = ContractSection.objects.filter(id__in=request.data['source_list'])
            contract_content = ''
            for selectedSection in selectedSections:
                contract_content += selectedSection.content

            instance.content = contract_content
            instance.save()

        return_serializer = ContractSerializer(instance)
        return Response(
            return_serializer.data, status=HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = Contract.objects.filter(id=self.kwargs['pk']).first()
        instance.content = request.data['content']
        instance.contact_emails = request.data['contact_emails']
        instance.start_date=request.data['start_date']
        instance.end_date=request.data['end_date']
        instance.live_edit = False
        instance.live_editor = None

        revision = ContractRevisions.objects.get(
            contract_id = instance.id,
            editor_id = request.user.id,
            live_edit = True
        )

        document = None
        try:
            document = request.data['document']
        except Exception as e:
            pass

        if document is not None:
            instance.document = document
            revision.document = document

        instance.save()

        revision.live_edit = False
        revision.content = request.data['content']
        revision.save()

        return_serializer = ContractSerializer(instance)
        return Response(
            return_serializer.data, status=HTTP_201_CREATED
        )

    @action(methods=['get'], detail=False, url_path='category/(?P<category_id>\d+)')
    def category_contracts(self, request, category_id):
        queryset = Contract.objects.filter(contract_for__model="category", target_id=category_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='job/(?P<job_id>\d+)')
    def job_contracts(self, request, job_id):
        queryset = Contract.objects.filter(contract_for__model="job", target_id=job_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='company/(?P<company_id>\d+)')
    def company_contracts(self, request, company_id):
        queryset = Contract.objects.filter(contract_with__model="company", entity_id=company_id)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='(?P<contract_id>\d+)/live_edit')
    def live_edit(self, request, contract_id):
        contract = Contract.objects.filter(id=contract_id).first()

        if contract.live_edit == False:
            contract.live_editor_id = request.user.id
            contract.live_edit = True
            contract.save()

            revision = ContractRevisions.objects.create(
                contract_id = contract.id,
                editor_id = request.user.id,
                content = contract.content,
                live_edit = True
            )

        serializer = self.get_serializer(contract)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='(?P<contract_id>\d+)/request_update')
    def request_update(self, request, contract_id):
        contract_revision = ContractRevisions.objects.filter(contract_id=contract_id, live_edit=True).first()

        if contract_revision != None:
            target = None

            if contract_revision.contract.contract_for.model == 'category':
                category = Category.objects.filter(id=contract_revision.contract.target_id).first()
                target = category.name
            if contract_revision.contract.contract_for.model == 'job':
                job = Job.objects.filter(id=contract_revision.contract.target_id).first()
                target = job.title

            contract_update_request_email(contract_revision.contract, target, request.user)

        serializer = self.get_serializer(contract_revision.contract)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='(?P<contract_id>\d+)/revisions')
    def contract_revisions(self, request, contract_id):
        queryset = ContractRevisions.objects.filter(contract_id=contract_id, live_edit=False)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='(?P<contract_id>\d+)/revision/(?P<revision_id>\d+)')
    def contract_revision(self, request, contract_id, revision_id):
        revisions = list(ContractRevisions.objects.filter(contract_id=contract_id, live_edit=False).order_by('id').values_list('id', flat=True))
        revision = ContractRevisions.objects.filter(id=revision_id, contract_id=contract_id, live_edit=False).first()

        if revision.changes == None or not revision.changes:
            revision_index = revisions.index(revision.id)

            compare_revision = None
            if revision_index == 0:
                compare_revision = revision.contract
            else:
                compare_index = revision_index - 1
                compare_revision = ContractRevisions.objects.get(id=revisions[compare_index])

            changes = contract_revision_changes(revision, compare_revision)

        serializer = self.get_serializer(revision, context={'request': request})

        return Response(serializer.data, status=HTTP_200_OK)

class ContractSectionView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractSectionListSerializer
        elif self.action == 'combine_sections':
            return ContractSectionsCombineSerializer
        else:
            return ContractSectionSerializer

    def get_queryset(self):
        return ContractSection.objects.all()

    @action(methods=['post'], detail=False, url_path='combine_sections')
    def combine_sections(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(request.data['source_list'])])
        selectedSections = ContractSection.objects.filter(id__in=request.data['source_list']).order_by(preserved)
        contract_content = ''
        for selectedSection in selectedSections:
            contract_content += selectedSection.content

        serializer = self.get_serializer({"content": contract_content})

        return Response(serializer.data, status=HTTP_200_OK)

class ContractTemplateView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return ContractTemplateListSerializer
        else:
            return ContractTemplateSerializer

    def get_queryset(self):
        return ContractTemplate.objects.all()

class ContractDocumentView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return ContractDocumentSerializer
        else:
            return ContractDocumentSerializer

    def get_queryset(self):
        return ContractDocument.objects.all()

class SupplierContractRevisionsView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == 'list':
            return SupplierContractRevisionsSerializer
        else:
            return SupplierContractRevisionsSerializer

    def get_queryset(self):
        return SupplierContractRevisions.objects.all()

    @action(methods=['get'], detail=False, url_path='last_revision')
    def last_revision(self, request):
        last_revision = SupplierContractRevisions.objects.last()

        serializer = self.get_serializer(last_revision)

        return Response(serializer.data, status=HTTP_200_OK)
