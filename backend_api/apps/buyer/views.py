import datetime
from django.shortcuts import render
from django import apps
from django.utils.timezone import make_aware
from django.db.models import Q, Count
from django.db.models.functions import TruncDate
from collections import Counter

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN
from .serializers import (
    CompanyListSerializer,
    CompanyCreateUpdateSerializer,
    BuyerListSerializer,
    BuyerCreateUpdateSerializer,
    BuyerRoleListSerializer,
    BuyerRoleCreateUpdateSerializer,
    BuyerRolePrivilegeListSerializer,
    BuyerRolePrivilegeCreateUpdateSerializer,
    BuyerPrivilegeListSerializer,
    BuyerPrivilegeCreateUpdateSerializer,
    BuyerPrivilegeListSummarySerializer,
)
from .models import Company, Buyer, BuyerRole, BuyerPrivilege, BuyerRolePrivilege
from apps.core.models import Job

from apps.core.serializers import JobsSerializer, LiveJobsSerializer
from apps.authentication.tokens import get_user_type

class CompanyView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    def get_serializer_class(self):
        if self.action == "list":
            return CompanyListSerializer
        return CompanyCreateUpdateSerializer

    def get_queryset(self):
        # print("got here")
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type == 'buyer':
            return Company.objects.filter(id=self.request.session["company_id"])
        else:
            return Company.objects.all().order_by("-id")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='list')
    def buyers_list(self, request):
        """
        Has no pagination
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    @action(methods=['get'], detail=False, url_path='dashboard')
    def dashboard(self, request):
        """
        Return buyer dashboard stats
        """
        company_id = self.request.auth.payload["company_id"]

        total_bidders = 0
        responsive_bidders = 0
        non_responsive_bidders = 0
        goods = 0
        services = 0
        works = 0

        jobs = apps.apps.get_model('core', 'Job').objects.filter(company_id=company_id)
        our_jobs = jobs.count()
        live_jobs = len([x for x in jobs if x.is_open])

        for job in jobs:
            if job.is_open:
                bidders = job.bidders
                total_bidders += bidders['total_bidders']    
                responsive_bidders += bidders['responsive_bidders']  
                non_responsive_bidders += bidders['non_responsive_bidders']  
                category_types = job.category_type_count
                goods += category_types['goods']    
                services += category_types['services']  
                works += category_types['works']  

        content = {
            "total_bidders": total_bidders,
            "responsive_bidders": responsive_bidders,
            "non_responsive_bidders": non_responsive_bidders,
            "bidders": [responsive_bidders, non_responsive_bidders],
            "live_jobs": live_jobs,
            "our_jobs": our_jobs,
            "goods": goods,
            "services": services,
            "works": works,
            "categories": [goods, services, works]
        }
        return Response(content, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='daily_bidders')
    def daily_bidders(self, request):
        """
        Return buyer dashboard daily bidders
        """
        company_id = self.request.auth.payload["company_id"]

        days = 14
        if self.request.query_params.get('days'):
            days = int(self.request.query_params.get('days'))      

        today = make_aware(datetime.datetime.today())
        dateslist = [(today - datetime.timedelta(days = day)).date() for day in reversed(range(days))]
        start_date = today - datetime.timedelta(days)

        prequal_responses = apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
            question__section__category__prequalification__company_id=company_id,
            created_at__gte=start_date
        ).distinct('question__section__category', 'supplier').values_list('created_at__date', flat=True)

        tender_responses = apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
            question__section__category__tender__company_id=company_id,
            created_at__gte=start_date
        ).distinct('question__section__category', 'supplier').values_list('created_at__date', flat=True)

        bidders = list(prequal_responses) + list(tender_responses)
        bidder_count = []
        for date in dateslist:
            bidder_count.append(bidders.count(date))

        content = {
            "daily_bidders": {
                "dates": dateslist,
                "bidder_count": bidder_count
            }
        }
        return Response(content, status=status.HTTP_200_OK)


class BuyerView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return BuyerListSerializer
        return BuyerCreateUpdateSerializer

    def get_queryset(self):
        # if "company_id" in self.request.session:
        #     return Buyer.objects.filter(
        #         company_id=self.request.session["company_id"]
        #     ).order_by("id")
        # else:
        print('got here')
        print(self.request.auth.payload['company_id'])
        users = Buyer.objects.filter(company_id=self.request.auth.payload['company_id']).order_by("id")
        print(users)
        return users

    def create(self, request, *args, **kwargs):
        # data = request.data.copy()
        # if 'company_id' in request.session:
        #     company = request.session['company_id']
        # else:
        #     company = self.kwargs['company_id']
        # data['company'] = company

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)      

    @action(methods=['get'], detail=False, url_path='my_privileges')
    def my_privileges(self, request):
        user = Buyer.objects.filter(id=self.request.auth.payload['user_id']).first()
        buyer_role_privileges = list(BuyerRolePrivilege.objects.filter(
            buyer_role_id=user.buyer_role.id,
            buyer_role__company_id=self.request.auth.payload['company_id'],
        ).values_list("buyer_privilege", flat=True))

        privileges = []

        buyer_privileges = BuyerPrivilege.objects.all()
        for buyer_privilege in buyer_privileges:
            has_privilege = False

            if buyer_privilege.id in buyer_role_privileges:
                privileges.append({
                    "id": buyer_privilege.id,
                    "title": buyer_privilege.title,
                    "has_privilege": True,
                    "description": buyer_privilege.description,
                    "created_at": buyer_privilege.created_at
                })

        serializer = BuyerPrivilegeListSummarySerializer(privileges, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)



class BuyerRoleView(viewsets.ModelViewSet):
    def get_queryset(self):
        # if self.request.session["company_id"]:
        #     return BuyerRole.objects.filter(
        #         company_id=self.request.session["company_id"]
        #     )
        # else:
        return BuyerRole.objects.filter(company_id=self.request.auth.payload['company_id'])

    def get_serializer_class(self):
        if self.action == "list":
            return BuyerRoleListSerializer
        return BuyerRoleCreateUpdateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class BuyerPrivilegeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return BuyerPrivilegeListSerializer
        return BuyerPrivilegeCreateUpdateSerializer

    def get_queryset(self):
        return BuyerPrivilege.objects.all().order_by('id')

    def create(self, request, *args, **kwargs):
        return Response()

    def update(self, request, *args, **kwargs):
        return Response()


class BuyerRolePrivilegeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return BuyerPrivilegeListSummarySerializer
        return BuyerRolePrivilegeCreateUpdateSerializer

    def get_queryset(self):
        if self.request.auth.payload['company_id']:
            buyer_role_privileges = list(BuyerRolePrivilege.objects.filter(
                buyer_role_id=self.kwargs["role_id"],
                buyer_role__company_id=self.request.auth.payload['company_id'],
            ).values_list("buyer_privilege", flat=True))

            privileges = []

            buyer_privileges = BuyerPrivilege.objects.all()
            for buyer_privilege in buyer_privileges:
                has_privilege = False

                if buyer_privilege.id in buyer_role_privileges:
                    has_privilege = True

                privileges.append({
                    "id": buyer_privilege.id,
                    "title": buyer_privilege.title,
                    "description": buyer_privilege.description,
                    "has_privilege": has_privilege,
                    "created_at": buyer_privilege.created_at
                })

            return privileges
        else:
            return BuyerRolePrivilege.objects.filter(
                buyer_role_id=self.kwargs["role_id"]
            )

    @action(methods=['delete'], detail=False, url_path='(?P<buyer_privilege_id>\d+)')
    def deny_privilege(self, request, role_id, buyer_privilege_id):
        buyer_role_privilege = BuyerRolePrivilege.objects.filter(
            buyer_role_id=role_id,
            buyer_privilege_id=buyer_privilege_id,
            buyer_role__company_id=self.request.auth.payload['company_id'],
        ).first()
        buyer_role_privilege.delete()

        return Response({},status=HTTP_204_NO_CONTENT)

class JobsView(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get',]

    def get_serializer_class(self):
        return JobsSerializer

    def get_queryset(self):
        return Job.objects.all()

    @action(methods=['get'], detail=False)
    def jobs_list(self, request):
        queryset = Job.objects.filter(company_id=request.auth.payload['company_id']).order_by('id')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='live_jobs')
    def live_jobs_list(self, request):
        jobs = Job.objects.filter(company_id=request.auth.payload['company_id']).order_by('id')
        queryset = [x for x in jobs if x.is_open]
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = LiveJobsSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = LiveJobsSerializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='company/(?P<company_id>\d+)')
    def buyer_jobs_list(self, request, company_id):
        user_type = get_user_type(self.request.auth.payload['user_id'])
        if user_type != 'qed':
            return Response({"error": "Invalid action"}, status=status.HTTP_403_FORBIDDEN)
            
        queryset = Job.objects.filter(company_id=company_id).order_by('id')
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=HTTP_200_OK)