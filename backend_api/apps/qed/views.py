import datetime
from dateutil.relativedelta import relativedelta
from io import BytesIO
from django import apps
from django.core.files import File
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import make_aware
from django.db.models import Q, Count
from django.db.models.functions import TruncDate, TruncMonth
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated

from apps.core.tasks import import_category_suppliers
from apps.prequal.reports import (
    bidder_locations_report, prequalified_suppliers_report, prequal_bidders_information_report,
    job_bidder_payments_report, responsive_bidders_report, non_responsive_bidders_report,
    directors_report, participation_status_report, QARankingReport, PrequalInterimReport, DueDiligenceRankingReport,
    prequal_evaluation_report_context
)

from apps.prequal.tasks import EvaluatePrequal, category_questions_upload
# from apps.prequal.utils import 
from apps.prequal.email_notifications import email_category_notifications, send_participants_email
from apps.core.utils import Render
from apps.qed import serializers
from apps.qed.models import Qed, QedPrivilege, QedRole, QedRolePrivilege
from apps.core.pagination import PageNumberPagination
from apps.core.serializers import JobsSerializer, LiveJobsSerializer
from apps.authentication.tokens import get_user_type

from apps.qed.serializers import (
    QedPrivilegeCreateUpdateSerializer,
    QedPrivilegeListSerializer,
    QedPrivilegeListSummarySerializer,
    QedRolePrivilegeSerializer,
    QedRoleSerializer,
    QedUserCreateUpdateSerializer,
    QedUserListSerializer,
)


class QedDashboardStatsView(viewsets.GenericViewSet):
    pagination_class = PageNumberPagination

    @action(methods=['get'], detail=False, url_path='stats')
    def stats(self, request):
        """
        Return buyer dashboard stats
        """
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type != 'qed':
            return Response({"error": "Unathorized access"}, status=status.HTTP_403_FORBIDDEN)

        jobs = apps.apps.get_model('core', 'Job').objects.filter().count()
        buyers = apps.apps.get_model('buyer', 'Company').objects.filter().count()
        suppliers = apps.apps.get_model('suppliers', 'SupplierCompany').objects.filter().count()

        content = {
            "jobs": jobs,
            "buyers": buyers,
            "suppliers": suppliers,
        }
        
        return Response(content, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='monthly_registration')
    def monthly_registration(self, request):
        months_before = 12
        today = make_aware(datetime.datetime.today())
        months12list = [(today - relativedelta(months = month)).date().replace(day=1) for month in reversed(range(months_before))]
        months12_start_date = months12list[0]

        supplier_registration = apps.apps.get_model('suppliers', 'SupplierCompany').objects.filter(created_at__gte=months12_start_date).annotate(month=TruncMonth('created_at__date')).values('month').annotate(total=Count('id'))
        supplier_registration_list = []
        for month in months12list:
            count = supplier_registration.filter(month=month).first()
            if count == None:
                supplier_registration_list.append(0)
            else:
                supplier_registration_list.append(count['total'])

        content = {
            "supplier_registration": {
                "dates": months12list,
                "reg_count": supplier_registration_list
            },
        }
        
        return Response(content, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='monthly_bids')
    def monthly_bids(self, request):
        months_before = 6
        today = make_aware(datetime.datetime.today())
        months6list = [(today - relativedelta(months = month)).date().replace(day=1) for month in reversed(range(months_before))]
        months6_start_date = months6list[0]

        monthly_bids = apps.apps.get_model('core', 'CategoryOrder').objects.filter(created_at__gte=months6_start_date).annotate(month=TruncMonth('created_at__date')).values('month').annotate(total=Count('id'))
        monthly_bids_list = []
        for month in months6list:
            count = monthly_bids.filter(month=month).first()
            if count == None:
                monthly_bids_list.append(0)
            else:
                monthly_bids_list.append(count['total'])

        content = {
            "monthly_bids": {
                "dates": months6list,
                "bids_count": monthly_bids_list
            },
        }
        
        return Response(content, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='live_jobs')
    def live_jobs(self, request):
        paginator = PageNumberPagination()

        jobs = apps.apps.get_model('core', 'Job').objects.all().order_by('id')
        queryset = [x for x in jobs if x.is_open]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LiveJobsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LiveJobsSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='jobs')
    def jobs(self, request):
        paginator = PageNumberPagination()

        queryset = apps.apps.get_model('core', 'Job').objects.all().order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = JobsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = JobsSerializer(queryset, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class QedView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return QedUserListSerializer
        else:
            return QedUserCreateUpdateSerializer

    def get_queryset(self):
        return Qed.objects.all().order_by('-id')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class QedRoleView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        return QedRoleSerializer

    def get_queryset(self):
        return QedRole.objects.all().order_by('-id')


class QedPriviledgeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return QedPrivilegeListSerializer
        return QedPrivilegeCreateUpdateSerializer

    def get_queryset(self):
        return QedPrivilege.objects.all().order_by('-id')


class QedRolePrivilegeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return QedPrivilegeListSummarySerializer
        return QedRolePrivilegeSerializer

    def get_queryset(self):
        qed_role_privileges = list(QedRolePrivilege.objects.filter(
            qed_role_id=self.kwargs["role_id"],
        ).values_list("qed_privilege", flat=True))

        privileges = []

        qed_privileges = QedPrivilege.objects.all()
        for qed_privilege in qed_privileges:
            has_privilege = False

            if qed_privilege.id in qed_role_privileges:
                has_privilege = True

            privileges.append({
                "id": qed_privilege.id,
                "title": qed_privilege.title,
                "description": qed_privilege.description,
                "has_privilege": has_privilege,
                "created_at": qed_privilege.created_at
            })

        return privileges


    @action(methods=['delete'], detail=False, url_path='(?P<qed_privilege_id>\d+)')
    def deny_privilege(self, request, role_id, qed_privilege_id):
        qed_role_privilege = QedRolePrivilege.objects.filter(
            qed_role_id=role_id,
            qed_privilege_id=qed_privilege_id,
        )
        qed_role_privilege.delete()

        return Response({},status=status.HTTP_204_NO_CONTENT)


class CategoryGroupView(viewsets.ModelViewSet):
    def get_queryset(self):
        return apps.apps.get_model('core', 'CategoryGroup').objects.all().order_by('id')

    def get_serializer_class(self):
        return serializers.CategoryGroupSerializer


class CategoryTypeView(viewsets.ModelViewSet):
    def get_queryset(self):
        return apps.apps.get_model('core', 'CategoryType').objects.all().order_by('id')

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.CategoryTypeCreateUpdateSerializer
        return serializers.CategoryTypeSerializer

    @action(methods=['post'], detail=False, url_path='upload/suppliers/(?P<category_id>\d+)')
    def upload_category_type_suppliers(self, request):
        # save file
        result = import_category_suppliers.delay(file_url=None)
        context = {
            'task_id': result.task_id,
            'response_message': 'Category supplier upload in progress'
        }
        return Response(context, status=status.HTTP_200_OK)


class CriteriaLocationView(viewsets.ModelViewSet):
    def get_queryset(self):
        return apps.apps.get_model('core', 'CriteriaCountry').objects.all().order_by('id')

    def get_serializer_class(self):
        return serializers.CriteriaLocationSerializer


class CriteriaCountryView(viewsets.ModelViewSet):
    def get_queryset(self):
        return apps.apps.get_model('core', 'CriteriaCountry').objects.all().order_by('id')

    def get_serializer_class(self):
        return serializers.CriteriaCountrySerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'category_type_id': kwargs['category_type_id']})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryTypeCriteriaView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return serializers.CategoryTypeCriteriaCreateUpdateSerializer
        return serializers.CategoryTypeCriteriaSerializer

    def get_queryset(self):
        return apps.apps.get_model('core', 'CategoryTypeCriteria').objects.all().order_by('id')

class JobsView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_serializer_class(self):
        return JobsSerializer

    def get_queryset(self):
        return apps.apps.get_model('core', 'Job').objects.all().order_by('-id')

    @action(methods=['get'], detail=False, url_path='buyer/(?P<company_id>\d+)')
    def jobs_list(self, request, company_id):
        queryset = apps.apps.get_model('core', 'Job').objects.filter(company_id=company_id).order_by('-id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)