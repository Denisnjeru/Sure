import datetime
from unicodedata import category
import pytz

from django import http, apps
from django.db import models
from django.utils import timezone
from django.utils.timezone import make_aware
from django.core.files import File
from django.db.models import Q, Value, F
from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, status, views, viewsets
from rest_framework.parsers import MultiPartParser, JSONParser, FormParser, FileUploadParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from decouple import config
from django.conf import settings

from . import serializers
from .serializers import (
    SupplierCompanyProfileRetrieveSerializer,
    SupplierCompanyProfileUpdateSerializer,
    SupplierCompanySerializer,
    SupplierCompanyUserCreateUpdateSerializer,
    SupplierCompanyUserSerializer,
    SupplierListSerializer,
    SupplierLoginSerializer,
    SupplierCreateUpdateSerializer,
    SupplierRFQSerializer,
    SupplierRolePrivilegeSerializer,
    SupplierRoleSerializer,
    SupplierPrivilegeListSummarySerializer
)
from .models import (
    Supplier,
    SupplierCompany,
    SupplierCompanyProfile,
    SupplierCompanyUser,
    SupplierPrivilege,
    SupplierRole,
    SupplierRolePrivilege,
)
from .utils import send_supplier_signup_email, generate_order_code

from apps.rfq import serializers as rfq_serializers
from apps.prequal import serializers as prequal_serializers
from apps.tender import serializers as tender_serializers
from apps.payments import views as payment_views
from apps.auction import serializers as auction_serializers
from .tasks import (
    send_tender_responses, create_tender_items_template, submit_tender_financial_responses, create_rfq_items_template
)
from apps.core.pagination import PageNumberPagination

# class SupplierRegisterView(generics.GenericAPIView):
#     """
#     Supplier Register View
#     """

#     serializer_class = SupplierCreateUpdateSerializer

#     def post(self, request):
#         supplier = request.data
#         serializer = self.serializer_class(data=supplier)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         user_data = serializer.data

#         supplier = Supplier.objects.get(email=user_data.get("email"))

#         # email verrification
#         # current_site = get_current_site(request).domain
#         # refresh = RefreshToken.for_user(supplier).access_token

#         # send_supplier_signup_email(
#         #     user=supplier, token=refresh, current_site=current_site
#         # )

#         return Response(user_data, status=status.HTTP_201_CREATED)
from ..prequal.utils import send_prequal_responses

class SupplierDashboardStatsView(viewsets.GenericViewSet):

    def list(self, request):
        supplier_id = self.request.auth.payload["user_id"]
        company_id = self.request.auth.payload["company_id"]

        users = SupplierCompanyUser.objects.filter(supplier_company_id=company_id).count()

        live_bids = 0
        closed_bids = 0
        bids = apps.apps.get_model('core', 'CategoryOrder').objects.filter(supplier_id=supplier_id, payment_status=1)
        for bid in bids:
            if bid.category != None:
                if bid.category.is_open == False:
                    closed_bids += 1
                else:
                    live_bids += 1


        award_letters = 0
        prequal_award_letters = apps.apps.get_model('prequal', 'AwardLetter').objects.filter(supplier_id=supplier_id).count()
        tender_award_letters = apps.apps.get_model('tender', 'AwardLetter').objects.filter(supplier_id=supplier_id).count()
        award_letters = prequal_award_letters + tender_award_letters

        regret_letters = 0
        prequal_regret_letters = apps.apps.get_model('prequal', 'RegretLetter').objects.filter(supplier_id=supplier_id).count()
        tender_regret_letters = apps.apps.get_model('tender', 'RegretLetter').objects.filter(supplier_id=supplier_id).count()
        regret_letters = prequal_regret_letters + tender_regret_letters

        letters = award_letters + regret_letters

        content = {
            "letters": letters,
            "users": users,
            "live_bids": live_bids,
            "closed_bids": closed_bids
        }

        return Response(content, status=status.HTTP_200_OK)
    
    @action(methods=['get'], detail=False, url_path='letters')
    def letters(self, request):
        paginator = PageNumberPagination()

        supplier_id = self.request.auth.payload["user_id"]

        query = Q()
        query |= Q(supplier_id=supplier_id)

        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            prequal_query =  Q()
            prequal_query |= Q(category__prequalification__company__company_name__icontains=search)
            prequal_query |= Q(category__name__icontains=search)
            prequal_query |= Q(category__prequalification__title__icontains=search)
            prequal_query &= query

            tender_query =  Q()
            tender_query |= Q(category__tender__company__company_name__icontains=search)
            tender_query |= Q(category__name__icontains=search)
            tender_query |= Q(category__tender__title__icontains=search)
            tender_query &= query
        else:
            prequal_query = query
            tender_query = query
        
        prequal_award_letters = apps.apps.get_model('prequal', 'AwardLetter').objects.filter(prequal_query).annotate(
            company=F('category__prequalification__company__company_name'), 
            job=F('category__prequalification__title'), 
            type=Value('Award', output_field=models.TextField()), 
            sourcing_activity=Value('prequal', output_field=models.TextField()),
            date=F('award_date'), 
        )
        tender_award_letters = apps.apps.get_model('tender', 'AwardLetter').objects.filter(tender_query).annotate(
            company=F('category__tender__company__company_name'), 
            job=F('category__tender__title'), 
            type=Value('Award', output_field=models.TextField()), 
            sourcing_activity=Value('tender', output_field=models.TextField()),
            date=F('award_date'), 
        )

        prequal_regret_letters = apps.apps.get_model('prequal', 'RegretLetter').objects.filter(prequal_query).annotate(
            company=F('category__prequalification__company__company_name'), 
            job=F('category__prequalification__title'), 
            type=Value('Regret', output_field=models.TextField()), 
            sourcing_activity=Value('prequal', output_field=models.TextField()),
            date=F('regret_date'), 
        )
        tender_regret_letters = apps.apps.get_model('tender', 'RegretLetter').objects.filter(tender_query).annotate(
            company=F('category__tender__company__company_name'), 
            job=F('category__tender__title'), 
            type=Value('Regret', output_field=models.TextField()), 
            sourcing_activity=Value('tender', output_field=models.TextField()),
            date=F('regret_date'), 
        )
        
        letters = list(prequal_award_letters) + list(tender_award_letters) + list(prequal_regret_letters) + list(tender_regret_letters)
        page = paginator.paginate_queryset(letters, request)
        if page is not None:
            serializer = serializers.LetterCategoriesSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.LetterCategoriesSerializer(letters, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierRegisterView(viewsets.ModelViewSet):
    http_method_names = ["post", "put", "patch"]

    def get_serializer_class(self):
        return SupplierCreateUpdateSerializer

    def get_queryset(self):
        return Supplier.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.queryset.get(pk=kwargs["pk"])
        serializer = self.serializer_class(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierView(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_serializer_class(self):
        return SupplierListSerializer

    def get_queryset(self):
        if "company_id" in self.request.auth.payload:
            return Supplier.objects.filter(
                company_id=self.request.auth.payload["company_id"]
            ).order_by("id")
        else:
            return Supplier.objects.all()


class SupplierCompanyView(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_serializer_class(self):
        return SupplierCompanySerializer

    def get_queryset(self):
        return SupplierCompany.objects.all()
        # return SupplierCompany.objects.select_related("admin_supplier").all()


class SupplierRoleView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        return SupplierRoleSerializer

    def get_queryset(self):
        if "company_id" in self.request.auth.payload:
            return SupplierRole.objects.filter(
                company_id=self.request.auth.payload["company_id"]
            ).order_by("id")
        else:
            return SupplierRole.objects.all()


class SupplierPrivilegeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        return SupplierRolePrivilegeSerializer

    def get_queryset(self):
        return SupplierPrivilege.objects.all()


class SupplierRolePrivilegeView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "list":
            return SupplierPrivilegeListSummarySerializer
        return SupplierRolePrivilegeSerializer

    def get_queryset(self):
        if self.request.auth.payload['company_id']:
            supplier_role_privileges = list(SupplierRolePrivilege.objects.filter(
                supplier_role_id=self.kwargs["role_id"],
                supplier_role__company_id=self.request.auth.payload['company_id'],
            ).values_list("supplier_privilege", flat=True))

            privileges = []

            supplier_privileges = SupplierPrivilege.objects.all()
            for supplier_privilege in supplier_privileges:
                has_privilege = False

                if supplier_privilege.id in supplier_role_privileges:
                    has_privilege = True

                privileges.append({
                    "id": supplier_privilege.id,
                    "title": supplier_privilege.title,
                    "description": supplier_privilege.description,
                    "has_privilege": has_privilege,
                    "created_at": supplier_privilege.created_at
                })

            return privileges
        else:
            return SupplierRolePrivilege.objects.filter(
                supplier_role_id=self.kwargs["role_id"]
            )

    @action(methods=['delete'], detail=False, url_path='(?P<supplier_privilege_id>\d+)')
    def deny_privilege(self, request, role_id, supplier_privilege_id):
        supplier_role_privilege = SupplierRolePrivilege.objects.filter(
            supplier_role_id=role_id,
            supplier_privilege_id=supplier_privilege_id,
            supplier_role__company_id=self.request.auth.payload['company_id'],
        ).first()
        supplier_role_privilege.delete()

        return Response({},status=status.HTTP_204_NO_CONTENT)



class SupplierCompanyUserView(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == "list":
            return SupplierCompanyUserSerializer
        return SupplierCompanyUserCreateUpdateSerializer

    def get_queryset(self):
        if "company_id" in self.request.auth.payload:
            return SupplierCompanyUser.objects.filter(
                supplier_company_id=self.request.auth.payload['company_id']
            ).order_by("id")
        else:
            return SupplierCompanyUser.objects.all()

    @action(methods=['get'], detail=False, url_path='my_privileges')
    def my_privileges(self, request):
        user = Supplier.objects.filter(id=self.request.auth.payload['user_id']).first()

        supplier_role_privileges = list(SupplierRolePrivilege.objects.filter(
            supplier_role_id=user.supplier_role.id,
            supplier_role__company_id=self.request.auth.payload['company_id'],
        ).values_list("supplier_privilege", flat=True))

        privileges = []

        supplier_privileges = SupplierPrivilege.objects.all()
        for supplier_privilege in supplier_privileges:
            has_privilege = False

            if supplier_privilege.id in supplier_role_privileges:

                privileges.append({
                    "id": supplier_privilege.id,
                    "title": supplier_privilege.title,
                    "has_privilege": True,
                    "description": supplier_privilege.description,
                    "created_at": supplier_privilege.created_at
                })

        serializer = serializers.SupplierPrivilegeListSummarySerializer(privileges, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierCompanyProfileView(viewsets.ModelViewSet):
    http_method_names = ["get", "patch"]
    parser_classes = (MultiPartParser,FormParser,FileUploadParser,)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SupplierCompanyProfileRetrieveSerializer
        return SupplierCompanyProfileUpdateSerializer

    def get_queryset(self):
        return SupplierCompanyProfile.objects.all()

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        print(serializer)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='company')
    def company_profile(self, request):
        profile = SupplierCompanyProfile.objects.filter(
            supplier_company_id=self.request.auth.payload["company_id"]
        ).first()

        serializer = serializers.SupplierCompanyProfileRetrieveSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompaniesWithOpenJobsView(viewsets.ModelViewSet):
    http_method_names = ['get',]

    def get_queryset(self):
        non_invite = apps.apps.get_model("buyer", "Company").objects.filter(
            Q(
                prequalification__category__is_open=True,
                prequalification__category__invite_only=False,
            )
            | Q(tender__category__is_open=True, tender__category__invite_only=False)
        )
        invite_in_prequal = apps.apps.get_model("prequal", "CategoryInvite").objects.filter(
            Q(supplier_id=self.request.auth.payload['user_id']) | Q(email=self.request.auth.payload['username']), category__is_open=True, category__invite_only=True
        ).values_list('category__prequalification__company', flat=True)  # get invite only jobs then get companies

        invite_in_tender = apps.apps.get_model("tender", "Invitee").objects.filter(
            Q(supplier_id=self.request.auth.payload['user_id']) | Q(email=self.request.auth.payload['username']), category__is_open=True, category__invite_only=True
        ).values_list('category__tender__company', flat=True)

        invite = list(invite_in_prequal) + list(invite_in_tender)
        invite = list(set(invite))
        invite_companies = apps.apps.get_model("buyer", "Company").objects.filter(id__in=invite)
        # compare between company objects in non_invite and invite
        companies = non_invite | invite_companies
        companies = companies.distinct()
        return companies

    def get_serializer_class(self):
        return serializers.BuyerCompanySerializer


class OpenPrequalJobsView(viewsets.ModelViewSet):
    http_method_names = ['get',]

    def get_queryset(self):
        return

    def get_serializer_class(self):
        return serializers.OrderedPrequalCategorySerializer

    @action(methods=['get'], detail=False, url_path='(?P<company_id>\d+)')
    def prequalifications(self, request, company_id):

        invite = apps.apps.get_model("prequal", "CategoryInvite").objects.filter(
            Q(supplier_id=self.request.auth.payload['user_id']) | Q(email=self.request.auth.payload['username']), 
            category__is_open=True, 
            category__invite_only=True,
            category__closing_date__gte=make_aware(datetime.datetime.now()),
            category__opening_date__lte=make_aware(datetime.datetime.now()),
            category__prequalification__company_id=company_id
        ).values_list('category', flat=True)

        categories = apps.apps.get_model("prequal", "Category").objects.filter(
            Q(
                is_open=True,
                invite_only=False,                
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
                prequalification__company_id=company_id,
                prequalification__status='final'
            ) |
            Q(
                is_open=True,
                invite_only=True,
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
                prequalification__company_id=company_id,
                prequalification__status='final',
                id__in=invite
            )

        )

        serializer = serializers.OrderedPrequalCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryOrderView(viewsets.ModelViewSet):

    def get_queryset(self):
        return apps.apps.get_model("core", "CategoryOrder").objects.filter(supplier_id=self.request.auth.payload['user_id'])

    def get_serializer_class(self):
        if self.action == 'mpesa_payment_stk':
            return serializers.CategoryOrderMpesaStkSerializer
        if self.action == 'cellulant_payment':
            return serializers.EmptySerializer
        if self.action == 'dpo_payment' or self.action == 'zero_charge':
            return serializers.EmptySerializer
        return serializers.CategoryOrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        selected_category = None
        ct = None
        if (request.data['target_name'] == 'prequal'):
            selected_category = apps.apps.get_model("prequal", "Category").objects.filter(
                id=request.data['category_id']
            ).first()
            ct = ContentType.objects.get(app_label='prequal', model="category")
        else:
            selected_category = apps.apps.get_model("tender", "Category").objects.filter(
                id=request.data['category_id']
            ).first()
            ct = ContentType.objects.get(app_label='tender', model="category")

        verify_category_order = apps.apps.get_model(
                'core', 'CategoryOrder'
            ).objects.filter(
                supplier_id=self.request.auth.payload['user_id'], category_id=request.data['category_id'], target=ct
            ).first()
        if verify_category_order != None:
            serializer = serializers.CategoryOrderSerializer(verify_category_order)
            return Response(serializer.data, status=status.HTTP_200_OK)

        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=apps.apps.get_model(
                'core', 'CategoryOrder'
            ).PENDING
        )

        code = None

        if (len(category_orders) > 0):
            category = None
            if (category_orders[0].target.name == 'Prequalification Category'):
                category = apps.apps.get_model("prequal", "Category").objects.filter(
                    id=category_orders[0].category_id
                ).first()
            else:
                category = apps.apps.get_model("tender", "Category").objects.filter(
                    id=category_orders[0].category_id
                ).first()


            if category.currency != selected_category.currency:
                return Response({"error": 'Different currencies'}, status=status.HTTP_400_BAD_REQUEST)

            code = category_orders[0].code
        else:
            code = generate_order_code()

        
        category_order =  apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.create(
            target=ct,category_id=request.data['category_id'],supplier_id=self.request.auth.payload['user_id'],code=code
        )
        print(category_order)
        serializer = serializers.CategoryOrderSerializer(category_order)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='categories')
    def categories_in_cart(self, request):
        paginator = PageNumberPagination()
        code = None
        prequal_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2, target__model='category', target__app_label='prequal',
        )

        if len(prequal_category_orders) > 0:
            code = prequal_category_orders[0].code

        prequals = prequal_category_orders.only('category_id').values('category_id')
        prequal_categories = apps.apps.get_model("prequal", "Category").objects.filter(
            id__in=prequals, is_open=True,
            closing_date__gte=make_aware(datetime.datetime.now()),
            opening_date__lte=make_aware(datetime.datetime.now()),
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(currency=F('currency__initials'), target=Value('prequal', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))

        # remove closed prequal categories from cart
        open_prequals = list(prequal_categories.values_list('id', flat=True))
        cart_prequals = list(prequals.values_list('category_id', flat=True))
        remove_prequals = list(set(open_prequals) ^ set(cart_prequals))
        apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            category_id__in=remove_prequals,supplier_id=self.request.auth.payload['user_id'], payment_status=2, target__model='category', target__app_label='prequal',
        ).delete()

        tender_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2, target__model='category', target__app_label='tender',
        )
        if len(tender_category_orders) > 0 and code != None:
            code = prequal_category_orders[0].code
        tenders = tender_category_orders.only('category_id').values('category_id')
        tender_categories = apps.apps.get_model("tender", "Category").objects.filter(
            id__in=tenders, is_open=True,
            closing_date__gte=make_aware(datetime.datetime.now()),
            opening_date__lte=make_aware(datetime.datetime.now()),
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(currency=F('currency__initials'), target=Value('tender', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))
        
        # remove closed tender categories from cart
        open_tenders = list(tender_categories.values_list('id', flat=True))
        cart_tenders = list(tenders.values_list('category_id', flat=True))
        remove_tenders = list(set(open_tenders) ^ set(cart_tenders))
        apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            category_id__in=remove_tenders,supplier_id=self.request.auth.payload['user_id'], payment_status=2, target__model='category', target__app_label='tender',
        ).delete()
        
        categories = list(prequal_categories) + list(tender_categories)

        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            serializer = serializers.CategoryOrderCategoriesSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.CategoryOrderCategoriesSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='ongoing_bids')
    def ongoing_bids(self, request):
        paginator = PageNumberPagination()

        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            prequal_query =  Q()
            prequal_query |= Q(prequalification__company__company_name__icontains=search)
            prequal_query |= Q(name__icontains=search)
            prequal_query |= Q(prequalification__title__icontains=search)

            tender_query =  Q()
            tender_query |= Q(tender__company__company_name__icontains=search)
            tender_query |= Q(name__icontains=search)
            tender_query |= Q(tender__title__icontains=search)
        else:
            prequal_query = Q()
            tender_query = Q()

        code = None
        prequal_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=1, target__model='category', target__app_label='prequal',
        )

        if len(prequal_category_orders) > 0:
            code = prequal_category_orders[0].code

        prequals = prequal_category_orders.only('category_id').values('category_id')
        prequal_categories = apps.apps.get_model("prequal", "Category").objects.filter(
            Q(
                id__in=prequals, is_open=True,
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
            ) & prequal_query
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(company=F('prequalification__company__company_name'), job=F('prequalification__title'), currency=F('currency__initials'), target=Value('prequal', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))

        tender_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=1, target__model='category', target__app_label='tender',
        )
        if len(tender_category_orders) > 0 and code != None:
            code = prequal_category_orders[0].code
        tenders = tender_category_orders.only('category_id').values('category_id')
        tender_categories = apps.apps.get_model("tender", "Category").objects.filter(
            Q(
                id__in=tenders, is_open=True,
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
            ) & tender_query
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(company=F('tender__company__company_name'), job=F('tender__title'), currency=F('currency__initials'), target=Value('tender', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))
        
        categories = list(prequal_categories) + list(tender_categories)

        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            serializer = serializers.CategoryOrderCategoriesSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.CategoryOrderCategoriesSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='closed_bids')
    def closed_bids(self, request):
        paginator = PageNumberPagination()

        if self.request.query_params.get('search'):
            search = self.request.query_params.get('search')
            prequal_query =  Q()
            prequal_query |= Q(prequalification__company__company_name__icontains=search)
            prequal_query |= Q(name__icontains=search)
            prequal_query |= Q(prequalification__title__icontains=search)

            tender_query =  Q()
            tender_query |= Q(tender__company__company_name__icontains=search)
            tender_query |= Q(name__icontains=search)
            tender_query |= Q(tender__title__icontains=search)
        else:
            prequal_query = Q()
            tender_query = Q()

        code = None
        prequal_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=1, target__model='category', target__app_label='prequal',
        )

        if len(prequal_category_orders) > 0:
            code = prequal_category_orders[0].code

        prequals = prequal_category_orders.only('category_id').values('category_id')
        prequal_categories = apps.apps.get_model("prequal", "Category").objects.filter(
            Q(
                id__in=prequals, is_open=False,
                closing_date__lte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
            ) & prequal_query
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(company=F('prequalification__company__company_name'), job=F('prequalification__title'), currency=F('currency__initials'), target=Value('prequal', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))

        tender_category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=1, target__model='category', target__app_label='tender',
        )
        if len(tender_category_orders) > 0 and code != None:
            code = prequal_category_orders[0].code
        tenders = tender_category_orders.only('category_id').values('category_id')
        tender_categories = apps.apps.get_model("tender", "Category").objects.filter(
            Q(
                id__in=tenders, is_open=False,
                closing_date__lte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
            ) & tender_query
        ).values('id', 'name', 'closing_date', 'bid_charge').annotate(company=F('tender__company__company_name'), job=F('tender__title'), currency=F('currency__initials'), target=Value('tender', output_field=models.TextField()), code=Value(code, output_field=models.TextField()))
        
        categories = list(prequal_categories) + list(tender_categories)

        page = paginator.paginate_queryset(categories, request)
        if page is not None:
            serializer = serializers.CategoryOrderCategoriesSerializer(page, many=True, context={'request': request})
            return paginator.get_paginated_response(serializer.data)

        serializer = serializers.CategoryOrderCategoriesSerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='remove')
    def remove_from_cart(self, request):
        ct = None
        if (request.data['target_name'] == 'prequal'):
            ct = ContentType.objects.get(app_label='prequal', model="category")
        else:
            ct = ContentType.objects.get(app_label='tender', model="category")

        category_order = apps.apps.get_model("core", "CategoryOrder").objects.filter(
            supplier_id=self.request.auth.payload['user_id'],
            category_id=self.request.data['category_id'],
            target=ct
        ).first()
        if category_order != None:
            category_order.delete()
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='payment/zero_charge')
    def zero_charge(self, request):
        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2
        )

        if len(category_orders) > 0:
            response = payment_views.make_zero_charge(category_orders)
            return Response(response,status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Unable to process the categories'},status=status.HTTP_400_BAD_REQUEST)


    @action(methods=['post'], detail=False, url_path='payment/mpesa')
    def mpesa_payment_stk(self, request):
        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2
        )

        phone_number = request.data['phone_number']
        if len(str(phone_number)) != 12:
            return Response({'error': 'Please validate phone number is in the correct format'}, status=status.HTTP_400_BAD_REQUEST)

        total = 0
        payment_ref = None
        for category_order in category_orders:
            payment_ref = category_order.code
            total += category_order.category.bid_charge

        total = float(total)
        stk_response = payment_views.STKPush(request,phone_number,total,payment_ref)

        if stk_response == 'error':
            return Response({'error': 'Error occurred while initiating request'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='payment/dpo')
    def dpo_payment(self, request):
        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2
        )

        total = 0
        payment_ref = None
        for category_order in category_orders:
            if category_order.category.is_open == True:
                if len(category_order.code) == 0:
                    if payment_ref == None:
                        code = generate_order_code()
                        category_order.code = code
                    else:
                        category_order.code = payment_ref
                    category_order.save()
                else:
                    payment_ref = category_order.code

                total += category_order.category.bid_charge
            else:
                category_order.delete()

        currency = "KES"
        if category_orders[0].category:
            if category_orders[0].category.currency == "KES":
                currency = "KES"
            if category_orders[0].category.currency == "USH":
                currency = "UGX"
            if category_orders[0].category.currency == "TSH":
                currency = "TZS"
            if category_orders[0].category.currency == "GHS":
                currency = "GHS"
            if category_orders[0].category.currency == "ZWD":
                currency = "ZWD"
            if category_orders[0].category.currency == "NGN":
                currency = "NGN"
            if category_orders[0].category.currency == "ZAR":
                currency = "ZAR"
            if category_orders[0].category.currency == "ZMW":
                currency = "ZMW"

        basket_amount = float(total)
        supplier = category_orders[0].supplier

        token = payment_views.dpo_get_token(
            amount=int(basket_amount),
            currency=currency,
            reference=payment_ref,
            supplier=supplier,
        )

        url = f"https://secure.3gdirectpay.com/pay.asp?ID={token}"

        return Response({"url": url},status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='payment/cellulant')
    def cellulant_payment(self, request):
        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=self.request.auth.payload['user_id'], payment_status=2
        )

        total = 0
        payment_ref = None
        for category_order in category_orders:
            if category_order.category.is_open == True:
                if len(category_order.code) == 0:
                    if payment_ref == None:
                        code = generate_order_code()
                        category_order.code = code
                    else:
                        category_order.code = payment_ref
                    category_order.save()
                else:
                    payment_ref = category_order.code

                total += category_order.category.bid_charge
            else:
                category_order.delete()

        currency = "KES"
        countryCode = "KE"
        if category_orders[0].category:
            if category_orders[0].category.currency == "KES":
                currency = "KES"
                countryCode = "UG"
            if category_orders[0].category.currency == "USH":
                currency = "UGX"
                countryCode = "KE"
            if category_orders[0].category.currency == "TSH":
                currency = "TZS"
                countryCode = "TZ"
            if category_orders[0].category.currency == "GHS":
                currency = "GHS"
            if category_orders[0].category.currency == "ZWD":
                currency = "ZWD"
            if category_orders[0].category.currency == "NGN":
                currency = "NGN"
            if category_orders[0].category.currency == "ZAR":
                currency = "ZAR"
            if category_orders[0].category.currency == "ZMW":
                currency = "ZMW"
                countryCode = "ZM"

        basket_amount = float(total)
        supplier = category_orders[0].supplier

        payload = {
            "merchantTransactionID": payment_ref,
            "customerFirstName": supplier.first_name,
            "customerLastName": supplier.last_name,
            "MSISDN": supplier.phone_number,
            "customerEmail": supplier.username,
            "requestAmount": int(basket_amount),
            "currencyCode": currency,
            "accountNumber": payment_ref,
            # "serviceCode": "QED",
            # test
            "serviceCode": config('CellulantserviceCode'),
            "dueDate": str(category_orders[0].category.closing_date),
            "requestDescription": "Tendersure Category Payment",
            "countryCode": countryCode,
            "languageCode": "en",
            "successRedirectUrl": config('CellulantSuccessRedirectUrl'),
            "failRedirectUrl": config('CellulantFailRedirectUrl'),
            "pendingRedirectUrl": config('CellulantPendingRedirectUrl'),
            "paymentWebhookUrl": config('CellulantPaymentWebhookUrl'),
        }

        response = payment_views.cellulant_payment(payload)


        return Response(response, status=status.HTTP_200_OK)


class OpenTenderJobsView(viewsets.ModelViewSet):
    def get_queryset(self):
        return

    def get_serializer_class(self):
        return serializers.OrderedTenderCategorySerializer

    @action(methods=['get'], detail=False, url_path='(?P<company_id>\d+)')
    def tenders(self, request, company_id):

        invite = apps.apps.get_model("tender", "Invitee").objects.filter(
            Q(supplier_id=self.request.auth.payload['user_id']) | Q(email=self.request.auth.payload['username']), 
            category__is_open=True, 
            category__invite_only=True,
            category__closing_date__gte=make_aware(datetime.datetime.now()),
            category__opening_date__lte=make_aware(datetime.datetime.now()),
            category__tender__company_id=company_id
        ).values_list('category', flat=True)

        categories = apps.apps.get_model('tender', 'Category').objects.filter(
            Q(
                is_open=True,
                invite_only=False,
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
                tender__company_id=company_id,
                tender__status='final'
            ) |
            Q(
                is_open=True,
                invite_only=True,
                closing_date__gte=make_aware(datetime.datetime.now()),
                opening_date__lte=make_aware(datetime.datetime.now()),
                tender__company_id=company_id,
                tender__status='final',
                id__in=invite
            )
        )

        serializer = serializers.OrderedTenderCategorySerializer(categories, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderedPreQualCategoryView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FormParser)

    def get_queryset(self):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=supplier.id, target__model='category', target__app_label='prequal', payment_status=1
        ).only('category_id').values('category_id')

        categories = apps.apps.get_model("prequal", "Category").objects.filter(
            id__in=category_orders
        )
        return categories.order_by('id')

    def get_serializer_class(self):
        if self.action == "supplier_profile_selection_bid":
            return serializers.SupplierProfileSelectionBidSerializer
        return serializers.OrderedPrequalCategorySerializer

    def create(self, request, *args, **kwargs):
        return

    def update(self, request, *args, **kwargs):
        return

    @action(methods=['get'], detail=False, url_path='participation/progress/(?P<category_id>\d+)')
    def participation_progress(self, request, category_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        responses = apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
            question__section__category_id=category_id, supplier_id=supplier.id
        )
        questions = apps.apps.get_model('prequal', 'Question').objects.filter(section__category_id=category_id)

        context = {
            "progress": int((float(responses.count()) / float(questions.count())) * 100),
            "total": questions.count()
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='sections/(?P<category_id>\d+)')
    def sections(self, request, category_id):
        sections = apps.apps.get_model('prequal', 'Section').objects.filter(
            category_id=category_id, parent_section_id__isnull=True
        ).order_by('id')
        serializer = serializers.PrequalSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='preview/sections/(?P<category_id>\d+)')
    def preview_sections(self, request, category_id):
        sections = apps.apps.get_model('prequal', 'Section').objects.filter(
            category_id=category_id).order_by('id')
        supplier_id = (
            apps.apps.get_model("suppliers", "Supplier")
                .objects.filter(id=request.auth.payload["user_id"])
                .first().id
        )
        serializer = serializers.PrequalPreviewSectionSerializer(
            sections, many=True, context={'request': request, 'supplier_id': supplier_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='questions/(?P<section_id>\d+)')
    def section_questions(self, request, section_id):
        questions = apps.apps.get_model('prequal', 'Question').objects.filter(section_id=section_id).order_by('id')
        serializer = serializers.PrequalQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='bid/(?P<question_id>\d+)')
    def bid(self, request, question_id):
        question = apps.apps.get_model('prequal', 'Question').objects.filter(id=question_id).first()

        category = apps.apps.get_model('prequal', 'Category').objects.filter(id=question.section.category_id).first()
        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)

        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        old_responses = apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        )

        data_copy = request.data.copy()
        data_copy['supplier'] = supplier.id
        # todo cater for array response
        if old_responses.count() > 0:
            # if question.answer_type != apps.apps.get_model('prequal', 'Question').TYPE_UPLOAD:
            serializer = serializers.PrequalSupplierResponse(data=data_copy, instance=old_responses.first())
            if serializer.is_valid():
                if question.answer_type == apps.apps.get_model('prequal', 'Question').TYPE_UPLOAD:
                    # archive the document first
                    pass
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.PrequalSupplierResponse(data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='profile/selection/bid/(?P<question_id>\d+)')
    def supplier_profile_selection_bid(self, request, question_id):
        question = apps.apps.get_model('prequal', 'Question').objects.filter(id=question_id).first()
        category = apps.apps.get_model('prequal', 'Category').objects.filter(id=question.section.category_id).first()
        file_type = request.data['file_type']
        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)

        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        profile = supplier.profile

        old_response = apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        ).first()

        file = ""
        if file_type == "registration_cert_url":
            file = profile.registration_cert_url
        elif file_type == "kra_pin_url":
            file = profile.kra_pin_url
        elif file_type == "kra_compliance_url":
            file = profile.kra_compliance_url
        elif file_type == "kra_trading_licence_url":
            file = profile.kra_trading_licence_url
        elif file_type == "cr_12_document_url":
            file = profile.cr_12_document_url
        # file = open(url, "rb")

        if old_response:
            if question.answer_type == apps.apps.get_model('prequal', 'Question').TYPE_UPLOAD:
                # archive the document first
                apps.apps.get_model('prequal', 'SupplierResponse').objects.update_or_create(
                    supplier_id=supplier.id, question_id=question_id,
                    defaults={"document_url": file},
                )
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if question.answer_type == apps.apps.get_model('prequal', 'Question').TYPE_UPLOAD:
                apps.apps.get_model('prequal', 'SupplierResponse').objects.create(
                    supplier_id=supplier.id, question_id=question_id,
                    document_url=file,
                )
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='submit/ratios/(?P<section_id>\d+)')
    def submit_ratios(self, request, section_id):
        section = apps.apps.get_model('prequal', 'Section').objects.filter(
            id=section_id
        ).first()
        category = section.category
        if not category.is_open:
            context = {
                "response_message": "Category is already closed"
            }
            return Response(context, status=status.HTTP_200_OK)
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        request_data = request.data
        request_data['supplier'] = supplier.id
        ratio_instance = apps.apps.get_model('prequal', 'FinancialRatio').objects.filter(
            section_id=section_id, supplier_id=supplier.id
        ).first()
        if ratio_instance:
            s = serializers.PrequalRatioSerializer(data=request_data, instance=ratio_instance)
        else:
            s = serializers.PrequalRatioSerializer(data=request_data)

        if s.is_valid():
            s.save()
            context = {
                'response_message': 'Ratios submitted'
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "errors": s.errors,
                "response_message": "An error occurred"
            }
            return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='finish/bid/(?P<category_id>\d+)')
    def finish_bid(self, request, category_id):
        category = apps.apps.get_model('prequal', 'Category').objects.filter(id=category_id).first()
        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        send_prequal_responses.delay(category_id=category_id, supplier_id=supplier.id)
        context = {
            "response_message": "Technical envelope submitted successfully"
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='delete/response/(?P<question_id>\d+)')
    def delete_document(self, request, question_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        response = apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        ).first()
        if response:
            response.delete()
            context = {
                "response_message": "Response deleted successfully"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "Invalid"
        }
        return Response(context, status=status.HTTP_200_OK)


class OrderedTenderCategoryView(viewsets.ModelViewSet):
    def get_queryset(self):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        category_orders = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=supplier.id, target__model='category', target__app_label='tender', payment_status=1
        ).only('category_id').values('category_id')

        categories = apps.apps.get_model('tender', 'Category').objects.filter(id__in=category_orders)
        return categories

    def get_serializer_class(self):
        if self.action == 'supplier_profile_selection_bid':
            return serializers.SupplierProfileSelectionBidSerializer
        if self.action == 'submit_advanced_financial_bid':
            return serializers.SupplierFinancialResponse
        return serializers.OrderedTenderCategorySerializer

    def create(self, request, *args, **kwargs):
        return

    def update(self, request, *args, **kwargs):
        return

    @action(methods=['get'], detail=False, url_path='t/participation/progress/(?P<category_id>\d+)')
    def t_participation_progress(self, request, category_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        responses = apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
            question__section__category_id=category_id, supplier_id=supplier.id
        )
        questions = apps.apps.get_model('tender', 'Question').objects.filter(section__category_id=category_id)
        if responses.count() > 0:
            progress = int((float(responses.count()) / float(questions.count())) * 100)
        else:
            progress = 0
            
        context = {
            "progress": progress,
            "total": questions.count()
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='sections/(?P<category_id>\d+)')
    def sections(self, request, category_id):
        sections = apps.apps.get_model('tender', 'Section').objects.filter(
            category_id=category_id, parent_section_id__isnull=True
        ).order_by('id')
        serializer = serializers.TenderSectionSerializer(sections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='preview/sections/(?P<category_id>\d+)')
    def preview_sections(self, request, category_id):
        sections = apps.apps.get_model('tender', 'Section').objects.filter(
            category_id=category_id).order_by('id')
        supplier_id = (
            apps.apps.get_model("suppliers", "Supplier")
                .objects.filter(id=request.auth.payload["user_id"])
                .first().id
        )
        serializer = serializers.TenderPreviewSectionSerializer(
            sections, many=True, context={'request': request, 'supplier_id': supplier_id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='questions/(?P<section_id>\d+)')
    def section_questions(self, request, section_id):
        questions = apps.apps.get_model('tender', 'Question').objects.filter(section_id=section_id).order_by('id')
        serializer = serializers.TenderQuestionSerializer(questions, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='bid/(?P<question_id>\d+)')
    def bid(self, request, question_id):
        question = apps.apps.get_model('tender', 'Question').objects.filter(id=question_id).first()

        category = apps.apps.get_model('tender', 'Category').objects.filter(id=question.section.category_id).first()
        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)

        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        old_responses = apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        )
        question = apps.apps.get_model('tender', 'Question').objects.filter(id=question_id).first()
        data_copy = request.data.copy()
        data_copy['supplier'] = supplier.id
        # todo cater for array response
        if old_responses.count() > 0:
            # if question.answer_type != apps.apps.get_model('prequal', 'Question').TYPE_UPLOAD:
            serializer = serializers.TenderSupplierResponse(data=data_copy, instance=old_responses.first())
            if serializer.is_valid():
                if question.answer_type == apps.apps.get_model('tender', 'Question').TYPE_UPLOAD:
                    # archive the document first
                    pass
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializers.TenderSupplierResponse(data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='profile/selection/bid/(?P<question_id>\d+)')
    def supplier_profile_selection_bid(self, request, question_id):
        question = apps.apps.get_model('tender', 'Question').objects.filter(id=question_id).first()
        category = apps.apps.get_model('tender', 'Category').objects.filter(id=question.section.category_id).first()
        file_type = request.data['file_type']

        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)

        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        profile = supplier.profile

        old_response = apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        ).first()

        file = ""
        if file_type == "registration_cert_url":
            file = profile.registration_cert_url
        elif file_type == "kra_pin_url":
            file = profile.kra_pin_url
        elif file_type == "kra_compliance_url":
            file = profile.kra_compliance_url
        elif file_type == "kra_trading_licence_url":
            file = profile.kra_trading_licence_url
        elif file_type == "cr_12_document_url":
            file = profile.cr_12_document_url
        # file = open(url, "rb")

        if old_response:
            if question.answer_type == apps.apps.get_model('tender', 'Question').TYPE_UPLOAD:
                # archive the document first
                apps.apps.get_model('tender', 'SupplierResponse').objects.update_or_create(
                    supplier_id=supplier.id, question_id=question_id,
                    defaults={"document_url": file},
                )
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            if question.answer_type == apps.apps.get_model('tender', 'Question').TYPE_UPLOAD:
                apps.apps.get_model('tender', 'SupplierResponse').objects.create(
                    supplier_id=supplier.id, question_id=question_id,
                    document_url=file,
                )
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=False, url_path='submit/ratios/(?P<section_id>\d+)')
    def submit_ratios(self, request, section_id):
        section = apps.apps.get_model('tender', 'Section').objects.filter(
            id=section_id
        ).first()
        category = section.category
        if not category.is_open:
            context = {
                "response_message": "Category is already closed"
            }
            return Response(context, status=status.HTTP_200_OK)
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        request_data = request.data
        request_data['supplier'] = supplier.id
        ratio_instance = apps.apps.get_model('tender', 'FinancialRatio').objects.filter(
            section_id=section_id, supplier_id=supplier.id
        ).first()
        if ratio_instance:
            s = serializers.TenderRatioSerializer(data=request_data, instance=ratio_instance)
        else:
            s = serializers.TenderRatioSerializer(data=request_data)

        if s.is_valid():
            s.save()
            context = {
                'response_message': 'Ratios submitted'
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "errors": s.errors,
                "response_message": "An error occurred"
            }
            return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='finish/technical/bid/(?P<category_id>\d+)')
    def finish_technical_bid(self, request, category_id):
        category = apps.apps.get_model('tender', 'Category').objects.filter(id=category_id).first()
        if not category.is_open:
            context = {
                'response_message': 'Category is already closed'
            }
            return Response(context, status=status.HTTP_200_OK)
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        send_tender_responses.delay(category_id=category_id, supplier_id=supplier.id)
        context = {
            "response_message": "Technical envelope submitted successfully"
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path="items/(?P<category_id>\d+)")
    def items(self, request, category_id):
        items = apps.apps.get_model('tender', 'Item').objects.filter(category_id=category_id).order_by('number')
        serializer = serializers.TenderItemSerializer(items, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["post"], detail=False, url_path="submit/item/response/(?P<category_id>\d+)")
    def submit_item_response(self, request, category_id):
        category = apps.apps.get_model('tender', 'Category').objects.filter(
            id=category_id
        ).first()
        if category is not None:
            if category.is_open:
                supplier = apps.apps.get_model(
                    "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

                response = apps.apps.get_model('tender', 'ItemResponse').objects.filter(
                    item_id=request.data['item'], supplier_id=supplier.id
                ).first()
                data_copy = request.data.copy()
                data_copy['supplier'] = supplier.id
                data_copy['value'] = request.data['total']
                if response is None:
                    serializer = serializers.TenderItemResponseCreateUpdateSerializer(data=data_copy)
                else:
                    serializer = serializers.TenderItemResponseCreateUpdateSerializer(data=data_copy, instance=response)

                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    context = {
                        'response_message': 'Invalid data'
                    }
                    return Response(context, status=status.HTTP_400_BAD_REQUEST)
            else:
                context = {
                    'response_message': 'Category is already closed'
                }
                return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                'response_message': 'Invalid'
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)
    
    @action(methods=['post'], detail=False, url_path="submit/advanced/bid/(?P<category_id>\d+)")
    def submit_advanced_financial_bid(self, request, category_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

        instance = apps.apps.get_model("tender", 'SupplierFinancialResponse').objects.filter(
            category_id=category_id, supplier_id=supplier.id).first()
        data_copy = request.data.copy()
        data_copy["supplier"] = supplier.id
        data_copy["category"] = category_id
        if instance:
            s = serializers.SupplierFinancialResponseCreateUpdateSerializer(data=data_copy, instance=instance)
        else:
            s = serializers.SupplierFinancialResponseCreateUpdateSerializer(data=data_copy)

        if s.is_valid():
            s.save()
            if not instance:
                instance = apps.apps.get_model("tender", 'SupplierFinancialResponse').objects.filter(
                    category_id=category_id, supplier_id=supplier.id).first()

            context = submit_tender_financial_responses(instance)
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "Form invalid"
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path="get/items/template/(?P<category_id>\d+)")
    def download_items_template(self, request, category_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        result = create_tender_items_template.delay(supplier_id=supplier.id, category_id=category_id)
        context = {
            "task_id": result.task_id,
            "response_message": "Template generation initiated successfully."
        }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='delete/response/(?P<question_id>\d+)')
    def delete_document(self, request, question_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        response = apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
            supplier_id=supplier.id, question_id=question_id
        ).first()
        if response:
            response.delete()
            context = {
                "response_message": "Response deleted successfully"
            }
            return Response(context, status=status.HTTP_200_OK)
        context = {
            "response_message": "Invalid"
        }
        return Response(context, status=status.HTTP_200_OK)


class SupplierRFQView(viewsets.ModelViewSet):
    def get_serializer_class(self):
        if self.action == "apply_rfq":
            return rfq_serializers.RfqCategoryRetrieveSerializer
        return SupplierRFQSerializer


    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return []
        supplier_id = self.request.auth.payload["user_id"]

        supplier = (
            apps.apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
        )
        if supplier is not None:
            rfq_invitations = (
                apps.apps.get_model("rfq", "RfqInvitee")
                .objects.filter(Q(supplier_id=supplier.id) | Q(email=supplier.email))
                .values_list("category", flat=True)
            )
            rfqs = (
                apps.apps.get_model("rfq", "Category")
                .objects.filter(id__in=rfq_invitations,status_open=True)
                .order_by("id")
            )

            return rfqs
        else:
            return

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)
    
    @action(methods=["get"], detail=False, url_path="apply/rfq/(?P<category_id>\d+)")
    def apply_rfq(self, request, category_id):
        rfq = (
            apps.apps.get_model("rfq", "Category")
            .objects.filter(id=category_id)
            .first()
        )
        serializer = self.get_serializer(rfq)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, url_path="supplier/rfq/participation_status/(?P<category_id>\d+)/(?P<supplier_id>\d+)")
    def supplier_participation_status(self, request, category_id, supplier_id):
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=supplier_id)
            .first()
        )
        if supplier is not None:
            sup_responses = apps.apps.get_model("rfq","RFQItemResponse").objects.filter(rfq_item__category_id=category_id).values_list("supplier", flat=True)
 
            if supplier.id in sup_responses:
                context = {"message":True}
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = {"message":False}
                return Response(context, status=status.HTTP_200_OK)
        else:
            context = {"message":False}
            return Response(context, status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=False, url_path="get/items/template/(?P<category_id>\d+)")
    def download_items_template(self, request, category_id):
        supplier = apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()
        result = create_rfq_items_template.delay(supplier_id=supplier.id, category_id=category_id)
        context = {
            "task_id": result.task_id,
            "response_message": "Template generation initiated successfully."
        }
        return Response(context, status=status.HTTP_200_OK)

class ArchiveView(viewsets.ModelViewSet):
    http_method_names = ["get"]

    def get_serializer_class(self):
        return SupplierListSerializer

    def get_queryset(self):
        if "company_id" in self.request.auth.payload:
            return Supplier.objects.filter(
                id=self.request.auth.payload["user_id"]
            ).order_by("id")
        else:
            return Supplier.objects.all()

    @action(methods=['get'], detail=False, url_path='companies')
    def get_companies(self, request):
        prequal_company_ids = apps.apps.get_model("prequal","SupplierResponse").objects.filter(
            question__answer_type=apps.apps.get_model("prequal","Question").TYPE_UPLOAD, supplier_id=self.request.auth.payload['user_id']
        ).values_list('question__section__category__prequalification__company', flat=True)

        tender_company_ids_technical = apps.apps.get_model("tender","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id']
        ).values_list('question__section__category__tender__company', flat=True) #.distinct('question__section__category__tender')
        tender_company_ids_financial = apps.apps.get_model("tender","SupplierFinancialResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id']
        ).values_list('category__tender__company', flat=True) #.distinct('category__tender')
        tender_company_ids = list(tender_company_ids_financial) + list(tender_company_ids_technical)

        rfq_category_ids = apps.apps.get_model("rfq","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id']
        ).values_list('category__rfq__company', flat=True)

        company_ids = list(prequal_company_ids) + tender_company_ids + list(rfq_category_ids)
        company_ids = list(set(company_ids))

        companies = apps.apps.get_model("buyer", "Company").objects.filter(id__in=company_ids)
        companies = serializers.BuyerCompanySerializer(companies, many=True).data
        return Response(companies, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='company/(?P<company_id>\d+)/jobs')
    def get_jobs(self, request, company_id):
        prequal_job_ids = apps.apps.get_model("prequal","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], question__section__category__prequalification__company=company_id
        ).distinct('question__section__category__prequalification').values_list('question__section__category__prequalification', flat=True)
        prequal_job_ids = list(set(prequal_job_ids))
        prequals = apps.apps.get_model("prequal","Prequalification").objects.filter(id__in=prequal_job_ids)
        prequals = prequal_serializers.JobListSerializer(prequals, many=True).data

        tender_job_ids_technical = apps.apps.get_model("tender","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], question__section__category__tender__company=company_id
        ).values_list('question__section__category__tender', flat=True)
        tender_job_ids_financial = apps.apps.get_model("tender","SupplierFinancialResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], category__tender__company=company_id
        ).values_list('category__tender', flat=True)
        tender_job_ids = list(tender_job_ids_technical) + list(tender_job_ids_financial)
        tender_job_ids = list(set(tender_job_ids))
        tenders = apps.apps.get_model("tender","Tender").objects.filter(id__in=tender_job_ids)
        tenders = tender_serializers.JobListSerializer(tenders, many=True).data

        rfq_job_ids = apps.apps.get_model("rfq","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], category__rfq__company=company_id
        ).values_list('category__rfq', flat=True)
        rfqs = apps.apps.get_model("rfq","Rfq").objects.filter(id__in=rfq_job_ids)
        rfqs = rfq_serializers.JobListSerializer(rfqs, many=True).data
        
        jobs = prequals + tenders + rfqs
        return Response(jobs, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='company/(?P<company_id>\d+)/categories')
    def get_categories(self, request, company_id):
        prequal_category_ids = apps.apps.get_model("prequal","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], question__section__category__prequalification__company=company_id
        ).values_list('question__section__category', flat=True)
        prequal_categories = apps.apps.get_model("prequal","Category").objects.filter(id__in=prequal_category_ids)
        prequal_categories = prequal_serializers.CategoryListSerializer(prequal_categories, many=True).data

        tender_category_ids_technical = apps.apps.get_model("tender","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], question__section__category__tender__company=company_id
        ).values_list('question__section__category', flat=True)
        tender_category_ids_financial = apps.apps.get_model("tender","SupplierFinancialResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], category__tender__company=company_id
        ).values_list('category', flat=True)
        tender_category_ids = list(tender_category_ids_technical) + list(tender_category_ids_financial)
        tender_categories = apps.apps.get_model("tender","Category").objects.filter(id__in=tender_category_ids)
        tender_categories = tender_serializers.CategoryListSerializer(tender_categories, many=True).data

        rfq_category_ids = apps.apps.get_model("rfq","SupplierResponse").objects.filter(
            supplier_id=self.request.auth.payload['user_id'], category__rfq__company=company_id
        ).values_list('category', flat=True)
        rfq_categories = apps.apps.get_model("rfq","Category").objects.filter(id__in=rfq_category_ids)
        rfq_categories = rfq_serializers.RfqCategorySerializer(rfq_categories, many=True).data
        
        categories = prequal_categories + tender_categories + rfq_categories
        return Response(categories, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False, url_path='documents/(?P<category_id>\d+)/(?P<job_type>\w+)')
    def get_archive_documents(self, request, category_id, job_type):
        documents = []
        other_documents = []
        
        if job_type == 'Prequal':
            documents = apps.apps.get_model("prequal","Question").objects.filter(
                answer_type=apps.apps.get_model("prequal","Question").TYPE_UPLOAD, section__category_id=category_id
            )
            
            technical_document = apps.apps.get_model("prequal","SupplierPDFResponse").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if technical_document != None:
                technical_document = technical_document.full_document_url

            other_documents.append({"name": "Technical Responses Document", "document_url": technical_document})

            letter = None

            award_letter = apps.apps.get_model("prequal","AwardLetter").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if award_letter != None:
                letter = award_letter.full_document_url
            else:
                regret_letter = apps.apps.get_model("prequal","RegretLetter").objects.filter(
                    category_id=category_id, supplier_id=self.request.auth.payload['user_id']
                ).first()
                if regret_letter != None:
                    letter = regret_letter.full_document_url
                else:
                    custom_letter = apps.apps.get_model("prequal","CustomLetter").objects.filter(
                        category_id=category_id, supplier_id=self.request.auth.payload['user_id']
                    ).first()
                    if custom_letter != None:
                        letter = custom_letter.full_document_url
            other_documents.append({"name": "Letter", "document_url": letter})

            duedil_letter = apps.apps.get_model("prequal","DueDilligenceLetter").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if duedil_letter != None:
                duedil_letter = duedil_letter.full_document_url
            other_documents.append({"name": "Due Diligence Letter", "document_url": duedil_letter})

            receipt = None
            category_order =apps.apps.get_model("core","CategoryOrder").objects.filter(payment_status=apps.apps.get_model("core","CategoryOrder").PAID, target=ContentType.objects.get_for_model(apps.apps.get_model("prequal","Category")),category_id=category_id).first()
            if category_order != None:
                receipt = apps.apps.get_model("core","SupplierReceipt").objects.filter(
                supplier_id=self.request.auth.payload['user_id'], reference=category_order.code
                ).first()
                if receipt != None:
                    receipt = receipt.full_document_url
            other_documents.append({"name": "Payment Receipt", "document_url": receipt})


            documents = prequal_serializers.QuestionArchiveSerializer(documents, many=True, context={'supplier_id': self.request.auth.payload['user_id']}).data
        
        if job_type == 'Tender':
            documents = apps.apps.get_model("tender","Question").objects.filter(
                answer_type=apps.apps.get_model("tender","Question").TYPE_UPLOAD, section__category_id=category_id
            )            

            technical_document = apps.apps.get_model("tender","SupplierPDFResponse").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if technical_document != None:
                technical_document = technical_document.full_document_url

            other_documents.append({"name": "Technical Responses Document", "document_url": technical_document})

            financial_document = apps.apps.get_model("tender","SupplierFinancialResponse").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if financial_document != None:
                financial_document = financial_document.full_document_url

            other_documents.append({"name": "Financial Responses Document", "document_url": financial_document})

            letter = None

            award_letter = apps.apps.get_model("tender","AwardLetter").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if award_letter != None:
                letter = award_letter.full_document_url
            else:
                regret_letter = apps.apps.get_model("tender","RegretLetter").objects.filter(
                    category_id=category_id, supplier_id=self.request.auth.payload['user_id']
                ).first()
                if regret_letter != None:
                    letter = regret_letter.full_document_url
                else:
                    custom_letter = apps.apps.get_model("tender","CustomLetter").objects.filter(
                        category_id=category_id, supplier_id=self.request.auth.payload['user_id']
                    ).first()
                    if custom_letter != None:
                        letter = custom_letter.full_document_url
            other_documents.append({"name": "Letter", "document_url": letter})

            duedil_letter = apps.apps.get_model("tender","DueDilligenceLetter").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if duedil_letter != None:
                duedil_letter = duedil_letter.full_document_url
            other_documents.append({"name": "Due Diligence Letter", "document_url": duedil_letter})

            receipt = None
            category_order =apps.apps.get_model("core","CategoryOrder").objects.filter(payment_status=apps.apps.get_model("core","CategoryOrder").PAID, target=ContentType.objects.get_for_model(apps.apps.get_model("tender","Category")),category_id=category_id).first()
            if category_order != None:
                receipt = apps.apps.get_model("core","SupplierReceipt").objects.filter(
                supplier_id=self.request.auth.payload['user_id'], reference=category_order.code
                ).first()
                if receipt != None:
                    receipt = receipt.full_document_url
            other_documents.append({"name": "Payment Receipt", "document_url": receipt})


            documents = tender_serializers.QuestionArchiveSerializer(documents, many=True, context={'supplier_id': self.request.auth.payload['user_id']}).data

        if job_type == 'RFQ':        
            financial_document = apps.apps.get_model("rfq","SupplierResponse").objects.filter(
                category_id=category_id, supplier_id=self.request.auth.payload['user_id']
            ).first()
            if financial_document != None:
                financial_document = financial_document.full_document_url

            other_documents.append({"name": "Financial Responses Document", "document_url": financial_document})

        return Response({'documents': documents, 'other_documents': other_documents}, status=status.HTTP_200_OK)

class ParticipatingAuctionView(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser, FormParser)


    def get_invites(self):
        return apps.apps.get_model("auction", "AuctionInvitee").objects.filter(
            supplier_id=self.request.auth['user_id'])
    
    def is_invited(self, auction_id):
        return apps.apps.get_model("auction", "AuctionInvitee").objects.filter(
            supplier_id=self.request.auth['user_id'], auction_id=auction_id).exists()

    def invited_auctions(self):
        invited_auctions = []
        for invite in self.get_invites():
            invited_auctions.append(invite.auction.id)
        return invited_auctions

    def get_supplier(self):
        return apps.apps.get_model(
            "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

    def previous_bid(self, auction_item_id):
        return apps.apps.get_model('auction', 'AuctionItemResponses').objects.filter(
            supplier_id=self.request.auth.payload['user_id'], auction_item_id=auction_item_id
        )
    

    def get_queryset(self):
        # For now only empty queryset
        return None

    # def get_queryset(self):
    #     supplier = apps.apps.get_model(
    #         "suppliers", "Supplier").objects.filter(id=self.request.auth.payload['user_id']).first()

    #     auction_item_responses = apps.apps.get        
    #     auctions = apps.apps.get_model("auction", "Auction"
    #         ).objects.filter(invite_only=False, status_open=False)
        
    #     for invited_auction in self.invited_auctions():
    #         if not invited_auction in self.invited_auctions():
    #             auctions.append(invited_auction)
        
    #     category_orders = apps.apps.get_model(
    #         'core', 'CategoryOrder'
    #     ).objects.filter(
    #         supplier_id=supplier.id, target__model='category', target__app_label='prequal', payment_status=1
    #     ).only('category_id').values('category_id')

    #     categories = apps.apps.get_model("prequal", "Category").objects.filter(
    #         id__in=category_orders
    #     )
    #     return categories.order_by('id')

    @action(methods=['get'], detail=False, url_path='responses/(?P<auction_id>\d+)')
    def auction_responses(self, request, auction_id):
        auction_responses = apps.apps.get_model('auction', 'AuctionItemResponses').objects.filter(
            auction_item__auction_id = auction_id, supplier_id=self.request.auth.payload['user_id'] 
        ).order_by('id')
        serializer = auction_serializers.SupplierAuctionBid(auction_responses, many=True, context={'request': request})
        return Response(serializer.data, status = status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='bid/(?P<auction_item_id>\d+)')
    def bid(self, request, auction_item_id):
        auction_item = apps.apps.get_model('auction', 'AuctionItems').objects.filter(id=auction_item_id).first()

        auction = apps.apps.get_model('auction', 'Auction').objects.filter(id=auction_item.auction_id).first()

        # Check if the auction if open
        if not auction.status_open:
            context = {
                'response_message': 'Auction is closed!'
            }
            print(context)
            return Response(data=context, status=status.HTTP_304_NOT_MODIFIED)
    
        # Check if invite only and if open
        if auction.invite_only:
            if not self.is_invited(auction.id):
                context = {
                    'response_message': 'You are not invited to participate in this auction!'
                }
                print(context)
                return Response(data=context, status=status.HTTP_304_NOT_MODIFIED)
        
        supplier = self.get_supplier()
        data_copy = request.data.copy()
        data_copy['supplier'] = supplier.id
        prev = self.previous_bid(auction_item_id)
        if  prev.count() > 0:
            serializer = auction_serializers.SupplierAuctionBid(data=data_copy, instance=prev.first())
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = auction_serializers.SupplierAuctionBid(data=data_copy)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)