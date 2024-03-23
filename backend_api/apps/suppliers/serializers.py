import datetime
import traceback
import random
import string

from django import apps
from django.contrib import auth
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from apps.authentication.models import User
from apps.common.utils import OneYear

from apps.suppliers.models import (
    Supplier,
    SupplierCompany,
    SupplierCompanyProfile,
    SupplierCompanyUser,
    SupplierRole,
    SupplierPrivilege,
    SupplierRolePrivilege,
    country_choices,
    location_choices,
)
from apps.suppliers.tasks import process_supplier_category_type_location_information, \
     save_tender_financial_ratio_responses, save_prequal_financial_ratio_responses
from apps.suppliers.utils import send_default_password_email, send_supplier_signup_email
from ..core.utils import hash, show


class SupplierListSerializer(serializers.ModelSerializer):
    """
    List all suppliers
    """

    class Meta:
        model = Supplier
        fields = [
            "id",
            "company_name",
            "short_name",
            "contact_name",
            "phone_number",
            "email",
            "kra_pin_number",
            "address",
            "country",
            "location",
        ]


class SupplierCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Supplier serializer
    """

    category_type_ids = serializers.ListField(
        required=False, child=serializers.IntegerField(), allow_null=True
    )
    supply_locations = serializers.ListField(
        required=False, child=serializers.CharField(), allow_null=True
    )
    country = serializers.CharField()
    location = serializers.CharField()

    email = serializers.CharField(
        max_length=100,
        required=True,
    )
    kra_pin_number = serializers.CharField(
        max_length=20,
        min_length=5,
        required=True,
    )
    phone_number = serializers.CharField(max_length=13, min_length=10)

    class Meta:
        model = Supplier
        fields = [
            "email",
            "company_name",
            "phone_number",
            "contact_name",
            "kra_pin_number",
            "address",
            "country",
            "location",
            "supplier_type",
            "category_type_ids",
            "supply_locations",
            "supplier_type",
        ]

    def validate(self, attrs):
        username = attrs.get("email", "")
        kra_pin_number = attrs.get("kra_pin_number", "")
        phone_number = attrs.get("phone_number", "")

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError(
                {"username": "A user with that username already exists"}
            )
        if Supplier.objects.filter(kra_pin_number=kra_pin_number).exists():
            raise serializers.ValidationError(
                {"kra_pin_number": "A supplier with tha Tax pin number already exists"}
            )
        if Supplier.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": "A user with that phone number already exists"}
            )

        return super().validate(attrs)

    def create(self, validated_data, *args, **kwargs):
        category_types = validated_data.pop("category_type_ids")
        supply_locations = validated_data.pop("supply_locations")

        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(8)
        )

        supplier_company = SupplierCompany.objects.create(
            # admin_supplier=instance,
            company_name=validated_data.get("company_name"),
            tax_pin_number=validated_data.get("kra_pin_number"),
            phone_number=validated_data.get("phone_number"),
            contact_name=validated_data.get("contact_name"),
            country=validated_data.get("country"),
        )
        supplier_company.save()

        role = SupplierRole.objects.filter(company_id=supplier_company.id).first()
        if role is None:
            role = SupplierRole.objects.create(name="Admin",company_id=supplier_company.id)

        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)

        instance.username = validated_data.get("email")
        instance.first_name = validated_data.get("company_name")
        instance.supplier_company_id=supplier_company.id
        instance.supplier_role_id=role.id
        instance.is_active = False
        instance.save()

        # send email with default password
        try:
            refresh = RefreshToken.for_user(instance).access_token
            send_supplier_signup_email(user=instance, token=refresh, password=password)

        except Exception as e:
            #capture exception sentry
            pass

        # process category types and supply locations
        process_supplier_category_type_location_information.delay(
            supplier_id=instance.id,
            category_type_ids=category_types,
            locations=supply_locations,
        )

        return instance


class SupplierLoginSerializer(serializers.ModelSerializer, TokenObtainPairSerializer):
    email = serializers.EmailField(max_length=255, min_length=3)
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)

    class Meta:
        model = Supplier
        fields = ["email", "password"]

    def validate(self, attrs):
        email = attrs.get("email", "")
        password = attrs.get("password", "")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid user credentials")

        data = super().validate(attrs)

        refresh = self.get_token(user)
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data


class SupplierCompanySerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField(required=False)
    email = serializers.SerializerMethodField(required=False)

    class Meta:
        model = SupplierCompany
        fields = [
            "id",
            "company_name",
            "tax_pin_number",
            "contact_name",
            "country",
            "phone_number",
            "address",
            "email"
        ]

    def get_address(self, obj):
        return ""

    def get_email(self, obj):
        return ""


class SupplierRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierRole
        fields = [
            "id",
            "name",
            "description",
            "company",
            "created_at"
        ]


class SupplierPrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierRolePrivilege
        fields = ["id", "title", "description"]


class SupplierRolePrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierRolePrivilege
        fields = ["id", "supplier_role", "supplier_privilege"]

class SupplierPrivilegeListSummarySerializer(serializers.ModelSerializer):
    has_privilege = serializers.BooleanField()

    class Meta:
        model = SupplierPrivilege
        fields = ["id", "title", "description", "has_privilege", "created_at"]


class SupplierCompanyUserCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierCompanyUser
        fields = ["id", "supplier_name", "supplier_email", "supplier_role"]

    def create(self, validated_data):
        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(8)
        )
        supplier_company_id = self.context["request"].auth.payload["company_id"]
        # if "company_id" in self.context["request"].session:
        #     supplier_company_id = supplier_company_id
        instance = self.Meta.model(supplier_company_id, **validated_data)
        if password is not None:
            instance.set_password(password)
        instance.username = validated_data.get("supplier_email")
        instance.supplier_company_id = supplier_company_id
        instance.save()

        # send email with default password
        try:
            refresh = RefreshToken.for_user(instance).access_token
            send_supplier_signup_email(user=instance, token=refresh, password=password)

        except Exception as e:
            #capture exception sentry
            pass

        return instance


class SupplierCompanyUserSerializer(serializers.ModelSerializer):
    supplier_role = SupplierRoleSerializer()

    class Meta:
        model = SupplierCompanyUser
        fields = ["id", "first_name", "last_name", "username", "last_login", "is_active", "supplier_company", "supplier_name", "supplier_role", "email", "date_joined"]


class SupplierCompanyProfileRetrieveSerializer(serializers.ModelSerializer):
    supplier_company = SupplierCompanySerializer(many=False)

    class Meta:
        model = SupplierCompanyProfile
        fields = [
            "id",
            "supplier_company",
            "registration_cert_url",
            "logo_url",
            "kra_pin_url",
            "kra_compliance_url",
            "kra_trading_licence_url",
            "cr_12_document_url",
            "kra_compliance_expiry_date",
            "kra_trading_licence_expiry_date",
        ]
        read_only_fields = ("id",)


class SupplierCompanyProfileUpdateSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False,source='supplier_company.company_name')
    contact_name = serializers.CharField(required=False,source='supplier_company.contact_name')
    phone_number = serializers.CharField(required=False,source='supplier_company.phone_number')

    class Meta:
        model = SupplierCompanyProfile
        fields = [
            "id",
            "company_name",
            "contact_name",
            "phone_number",
            "registration_cert_url",
            "logo_url",
            "kra_pin_url",
            "kra_compliance_url",
            "kra_trading_licence_url",
            "cr_12_document_url",
            "kra_compliance_expiry_date",
            "kra_trading_licence_expiry_date",
        ]

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        for f in self.Meta.model._meta.get_fields():
            # Hack to always allow_null on FileFields
            if isinstance(f, serializers.FileField):
                kwargs = extra_kwargs.get(f.name, {})
                kwargs['allow_null'] = True
                extra_kwargs[f.name] = kwargs
        return extra_kwargs

    def validate(self, attrs):
        """
        Validate suplier profile data on profile update
        """
        date_today = datetime.datetime.now().date()
        kra_compliance_expiry_date = attrs.get("kra_compliance_expiry_date")
        kra_trading_licence_expiry_date = attrs.get("kra_trading_licence_expiry_date")

        if kra_compliance_expiry_date != None:
            if kra_compliance_expiry_date < date_today:
                raise serializers.ValidationError(
                    {
                        "kra_compliance_expiry_date": "Your Expiry_date cannot be before today!"
                    }
                )
            
        if kra_trading_licence_expiry_date != None:
            if kra_trading_licence_expiry_date > OneYear(
                date_today.year, date_today.month, date_today.day
            ):
                raise serializers.ValidationError(
                    {
                        "kra_trading_licence_expiry_date": "Your Expiry_date cannot be further than a year from today!"
                    }
                )

        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.registration_cert_url = validated_data.get(
            "registration_cert_url", instance.registration_cert_url
        )
        instance.logo_url = validated_data.get("logo_url", instance.logo_url)
        instance.kra_pin_url = validated_data.get("kra_pin_url", instance.kra_pin_url)
        instance.kra_compliance_url = validated_data.get(
            "kra_compliance_url", instance.kra_compliance_url
        )
        instance.cr_12_document_url = validated_data.get(
            "cr_12_document_url", instance.cr_12_document_url
        )
        instance.kra_compliance_expiry_date = validated_data.get(
            "kra_compliance_expiry_date", instance.kra_compliance_expiry_date
        )
        instance.kra_trading_licence_expiry_date = validated_data.get(
            "kra_trading_licence_expiry_date", instance.kra_trading_licence_expiry_date
        )
        instance.save()

        return instance


class OpenPrequalCategorySerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    payed_for = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Category")
        fields = [
            "id",
            "name",
            "trans_name",
            "unique_reference",
            "bid_charge",
            "currency",
            "opening_date",
            "closing_date",
            "is_open",
            "prequalification",
            "invite_only",
            "payed_for",
        ]
        ref_name = "OpenPrequalCategorySerializer"

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%dT%H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%dT%H:%M")

    def get_payed_for(self, obj):
        return


class OrderedPrequalCategorySerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    payed_for = serializers.SerializerMethodField()
    participated = serializers.SerializerMethodField()
    report = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Category")
        fields = [
            "id",
            "name",
            "trans_name",
            "unique_reference",
            "bid_charge",
            "currency",
            "opening_date",
            "closing_date",
            "is_open",
            "invite_only",
            "prequalification",
            "payed_for",
            "participated",
            "report",
        ]
        ref_name = "OpenPrequalCategorySerializer"
        depth = 2

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%d %H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%d %H:%M")

    def get_payed_for(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]

        category_order = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=user_id, category_id=obj.id,
            target = ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Category'))
        ).first()
       

        if category_order == None:
            return None
        else:
            return category_order.get_payment_status_display()

    def get_participated(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=user_id)
            .first()
        )
        if (
            apps.apps.get_model("prequal", "SupplierResponse")
            .objects.filter(supplier_id=supplier.id)
            .count()
            > 0
        ):
            return True
        else:
            return False

    def get_report(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=user_id)
            .first()
        )
        r = (
            apps.apps.get_model("prequal", "SupplierPDFResponse")
            .objects.filter(supplier_id=supplier.id, category_id=obj.id)
            .first()
        )
        if r is not None:
            return r.document_url.url
        else:
            return None


class PrequalCategoryInstructionsSerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Category")
        fields = [
            "id",
            "name",
            "trans_name",
            "unique_reference",
            "bid_charge",
            "currency",
            "opening_date",
            "closing_date",
            "is_open",
            "invite_only",
            "prequalification",
            "payed_for",
            "participated",
        ]
        ref_name = "OpenPrequalCategorySerializer"
        depth = 2

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%dT%H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%dT%H:%M")

    def get_payed_for(self, obj):
        return

    def get_participated(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=user_id)
            .first()
        )
        if (
            apps.apps.get_model("prequal", "SupplierResponse")
            .objects.filter(supplier_id=supplier.id)
            .count()
            > 0
        ):
            return True
        else:
            return False


class OrderedTenderCategorySerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    payed_for = serializers.SerializerMethodField()
    participated = serializers.SerializerMethodField()
    items_template = serializers.SerializerMethodField()
    previous_bid_template = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Category")
        fields = [
            "id", "name", "trans_name", "unique_reference", "bid_charge", "currency",
            "opening_date", "closing_date", "is_open", "invite_only", "tender",
            "payed_for", "participated", "rfq_type", "items_template", "previous_bid_template"
        ]
        ref_name = "OpenTenderCategorySerializer"
        depth = 2

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%d %H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%d %H:%M")

    def get_payed_for(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]

        category_order = apps.apps.get_model(
            'core', 'CategoryOrder'
        ).objects.filter(
            supplier_id=user_id, category_id=obj.id,
            target = ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Category'))
        ).first()

        if category_order == None:
            return None
        else:
            return category_order.get_payment_status_display()

    def get_participated(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = apps.apps.get_model("suppliers", "Supplier").objects.filter(id=user_id).first()
        if (apps.apps.get_model("tender", "SupplierResponse").objects.filter(supplier_id=supplier.id)
            .count()> 0):
            return True
        else:
            return False

    def get_items_template(self, obj):
        return obj.items_template.url

    def get_previous_bid_template(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=user_id)
            .first()
        )
        response = apps.apps.get_model("tender", "SupplierFinancialResponse").objects.filter(
            supplier_id=supplier.id, category_id=obj.id
        ).first()
        if response is not None:
            if response.excel_url is not None:
                return response.excel_url.url
        return None


class OpenPrequalJob(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("prequal", "Prequalification")
        fields = [
            "id",
            "company",
            "title",
            "unique_reference",
            "status",
            "lang_en",
            "show_bids",
            "advert",
            "bidding_instructions",
        ]

class CategoryOrderSerializer(serializers.ModelSerializer):
    payment_status = serializers.SerializerMethodField()
    target_name = serializers.CharField(required=False)
    class Meta:
        model = apps.apps.get_model("core", "CategoryOrder")
        fields = ["id", "target", "target_name", "category_id", "supplier", "payment_status"]

    def get_payment_status(self, obj):
        return obj.get_payment_status_display()

class CategoryOrderCategoriesSerializer(serializers.Serializer):
    name = serializers.CharField(allow_blank=True, required=False)
    id = serializers.IntegerField()
    target = serializers.CharField()
    bid_charge = serializers.IntegerField()
    closing_date = serializers.DateTimeField()
    currency = serializers.CharField()
    code = serializers.CharField()
    job = serializers.CharField(allow_blank=True, required=False)
    company = serializers.CharField(allow_blank=True, required=False)

class LetterCategoriesSerializer(serializers.Serializer):
    category = serializers.CharField(allow_blank=True, required=False, source='category.name')
    category_id = serializers.CharField(allow_blank=True, required=False, source='category.id')
    id = serializers.IntegerField()
    type = serializers.CharField()
    sourcing_activity = serializers.CharField()
    job = serializers.CharField(allow_blank=True, required=False)
    company = serializers.CharField(allow_blank=True, required=False)
    letter = serializers.SerializerMethodField()
    date = serializers.DateTimeField()

    def get_letter(self, obj):
        if obj.sourcing_activity == 'prequal' and obj.type == 'Award':
            letter = apps.apps.get_model('prequal', 'AwardLetter').objects.get(id=obj.id)
            return letter.letter.url
        elif obj.sourcing_activity == 'prequal' and obj.type == 'Regret':
            letter = apps.apps.get_model('prequal', 'RegretLetter').objects.get(id=obj.id)
            return letter.letter.url
        elif obj.sourcing_activity == 'tender' and obj.type == 'Award':
            letter = apps.apps.get_model('tender', 'AwardLetter').objects.get(id=obj.id)
            return letter.letter.url
        elif obj.sourcing_activity == 'tender' and obj.type == 'Regret':
            letter = apps.apps.get_model('tender', 'RegretLetter').objects.get(id=obj.id)
            return letter.letter.url
        else:
            return None

class CategoryOrderMpesaStkSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

class OpenTenderJob(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("tender", "Tender")
        fields = [
            "id",
            "company",
            "title",
            "unique_reference",
            "status",
            "lang_en",
            "show_bids",
            "advert",
            "bidding_instructions",
        ]


class BuyerCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("buyer", "Company")
        fields = [
            "id",
            "company_name",
            "phone_number",
            "contact_name",
            "company_logo_url",
            "buyer_initials",
        ]


class PrequalQuestionPreviewSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Question")
        fields = [
            "id", "description", "answer_type",
            "trans_description", "response",
        ]

    def get_response(self, obj):
        supplier_id = self.context['supplier_id']
        response = (
            apps.apps.get_model("prequal", "SupplierResponse")
            .objects.filter(supplier_id=supplier_id, question_id=obj.id)
            .first()
        )
        return PrequalSupplierResponse(response, many=False).data


class PrequalQuestionSerializer(serializers.ModelSerializer):
    marking_scheme = serializers.SerializerMethodField()
    response = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Question")
        fields = [
            "id",
            "section",
            "description",
            "answer_type",
            "trans_description",
            "is_required",
            "marking_scheme",
            "response",
        ]

    def get_marking_scheme(self, obj):
        ms = (
            apps.apps.get_model("prequal", "MarkingScheme")
            .objects.filter(question_id=obj.id)
            .first()
        )
        return PrequalMarkingSchemeSerializer(ms, many=False).data

    def get_response(self, obj):
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=self.context["request"].auth.payload["user_id"])
            .first()
        )
        response = (
            apps.apps.get_model("prequal", "SupplierResponse")
            .objects.filter(supplier_id=supplier.id, question_id=obj.id)
            .first()
        )
        return PrequalSupplierResponse(response, many=False).data


class PrequalMarkingSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("prequal", "MarkingScheme")
        fields = ["id", "options"]


class PrequalPreviewSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    financial_ratios = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Section")
        fields = [
            "id", "name", "description", "questions", "financial_ratios"
        ]

    def get_questions(self, obj):
        questions = apps.apps.get_model('prequal', 'Question').objects.filter(
            section_id=obj.id
        ).order_by('id')
        s = PrequalQuestionPreviewSerializer(
            questions, many=True,
            context={'request': self.context['request'], 'supplier_id': self.context['supplier_id']}
        )
        return s.data

    def get_financial_ratios(self, obj):
        section = apps.apps.get_model('prequal', 'Section').objects.filter(
            name='Financial Ratios', id=obj.id
        ).first()

        if section:
            ratios = apps.apps.get_model('prequal', 'FinancialRatio').objects.filter(
                section_id=obj.id, supplier_id=self.context['supplier_id']
            ).first()
            return PrequalFinancialRatioSerializer(ratios, many=False).data
        else:
            return


class PrequalFinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('prequal', 'FinancialRatio')
        fields = [
            "id", "equity", "curr_liabilities", "debtors", "turnover", "gross_profit", "net_profit",
            "cash", "fixed_assets", "current_assets"
        ]


class PrequalSectionSerializer(serializers.ModelSerializer):
    child_sections = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("prequal", "Section")
        fields = [
            "id",
            "name",
            "description",
            "category",
            "parent_section",
            "child_sections",
        ]

    def get_child_sections(self, obj):
        child_sections = apps.apps.get_model("prequal", "Section").objects.filter(
            parent_section_id=obj.id
        )
        return PrequalSectionSerializer(child_sections, many=True).data

    # def get_questions(self, obj):
    #     qs = apps.apps.get_model('prequal', 'Question').objects.filter()
    #     return


class PrequalSupplierResponse(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("prequal", "SupplierResponse")
        fields = ["question", "supplier", "document_url", "options"]


class TenderSectionSerializer(serializers.ModelSerializer):
    child_sections = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Section")
        fields = [
            "id",
            "name",
            "description",
            "category",
            "parent_section",
            "child_sections",
        ]

    def get_child_sections(self, obj):
        child_sections = apps.apps.get_model("tender", "Section").objects.filter(
            parent_section_id=obj.id
        )
        return TenderSectionSerializer(child_sections, many=True).data


class TenderQuestionSerializer(serializers.ModelSerializer):
    marking_scheme = serializers.SerializerMethodField()
    response = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Question")
        fields = [
            "id",
            "section",
            "description",
            "answer_type",
            "trans_description",
            "is_required",
            "marking_scheme",
            "response",
        ]

    def get_marking_scheme(self, obj):
        ms = (
            apps.apps.get_model("tender", "MarkingScheme")
            .objects.filter(question_id=obj.id)
            .first()
        )
        return TenderMarkingSchemeSerializer(ms, many=False).data

    def get_response(self, obj):
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=self.context["request"].auth.payload["user_id"])
            .first()
        )
        response = (
            apps.apps.get_model("tender", "SupplierResponse")
            .objects.filter(supplier_id=supplier.id, question_id=obj.id)
            .first()
        )
        return TenderSupplierResponse(response, many=False).data


class TenderMarkingSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("tender", "MarkingScheme")
        fields = ["id", "options"]


class TenderSupplierResponse(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("tender", "SupplierResponse")
        fields = ["question", "supplier", "document_url", "options"]


class TenderItemSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Item")
        fields = [
            "id",
            "number",
            "description",
            "unit_of_measure",
            "quantity",
            "response",
            "specification_1",
            "specification_2",
        ]

    def get_response(self, obj):
        user_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=user_id)
            .first()
        )
        response = (
            apps.apps.get_model("tender", "ItemResponse")
            .objects.filter(item_id=obj.id, supplier_id=supplier.id)
            .first()
        )

        return TenderItemResponseSerializer(response, many=False).data


class TenderItemResponseSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "ItemResponse")
        fields = ["id", "total", "item_number", "unit_price", "value", "item"]

    def get_total(self, obj):
        try:
            return float(show(obj.total))
        except:
            return obj.total


class TenderItemResponseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("tender", "ItemResponse")
        fields = [
            "id",
            "total",
            "item_number",
            "unit_price",
            "item",
            "supplier",
            "value",
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            t = hash(validated_data.pop('total'))
            instance = ModelClass._default_manager.create(**validated_data, total=t)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        t = hash(validated_data.pop('total'))
        instance.total = t
        instance.save()

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

class SupplierRFQSerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    supplier_participation_status = serializers.SerializerMethodField()
    job = serializers.CharField(read_only=True, source="rfq.title")
    company_name = serializers.CharField(
        read_only=True, source="rfq.company.company_name"
    )

    class Meta:
        model = apps.apps.get_model("rfq", "Category")
        fields = [
            "id",
            "name",
            "rfq",
            "category_type",
            "unique_reference",
            "opening_date",
            "closing_date",
            "evaluation_date",
            "unique_reference",
            "status_open",
            "invite_notification",
            "instructions",
            "self_evaluate",
            "rfq_type",
            "vatable",
            "vat_rate",
            "supplier_participation_status",
            "job",
            "company_name",
        ]

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%d %H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%d %H:%M")

    def get_supplier_participation_status(self,obj):
        supplier_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.apps.get_model("suppliers", "Supplier")
            .objects.filter(id=supplier_id)
            .first()
        )
        if supplier is not None:
            sup_responses = apps.apps.get_model("rfq","RFQItemResponse").objects.filter(rfq_item__category_id=obj.id).values_list("supplier", flat=True)

            if supplier.id in sup_responses:
                return True
            else:
                return False
        else:
            return False


class PrequalRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('prequal', 'FinancialRatio')
        fields = [
            'id', 'supplier', 'section', 'equity', 'curr_liabilities',
            'fixed_assets', 'current_assets', 'debtors', 'turnover',
            'gross_profit', 'net_profit', 'cash'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            save_prequal_financial_ratio_responses(instance_id=instance.id)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        save_prequal_financial_ratio_responses.delay(instance_id=instance.id)

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class TenderRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('tender', 'FinancialRatio')
        fields = [
            'id', 'supplier', 'section', 'equity', 'curr_liabilities',
            'fixed_assets', 'current_assets', 'debtors', 'turnover',
            'gross_profit', 'net_profit', 'cash'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            save_tender_financial_ratio_responses.delay(instance_id=instance.id)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                    'Got a `TypeError` when calling `%s.%s.create()`. '
                    'This may be because you have a writable field on the '
                    'serializer class that is not a valid argument to '
                    '`%s.%s.create()`. You may need to make the field '
                    'read-only, or override the %s.create() method to handle '
                    'this correctly.\nOriginal exception was:\n %s' %
                    (
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        ModelClass.__name__,
                        ModelClass._default_manager.name,
                        self.__class__.__name__,
                        tb
                    )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        save_tender_financial_ratio_responses.delay(instance_id=instance.id)

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class TenderPreviewSectionSerializer(serializers.ModelSerializer):
    questions = serializers.SerializerMethodField()
    financial_ratios = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Section")
        fields = [
            "id", "name", "description", "questions", "financial_ratios"
        ]

    def get_questions(self, obj):
        questions = apps.apps.get_model('tender', 'Question').objects.filter(
            section_id=obj.id
        )
        s = TenderQuestionPreviewSerializer(
            questions, many=True,
            context={'request': self.context['request'], 'supplier_id': self.context['supplier_id']}
        )
        return s.data

    def get_financial_ratios(self, obj):
        section = apps.apps.get_model('tender', 'Section').objects.filter(
            name='Financial Ratios', id=obj.id
        ).first()

        if section:
            ratios = apps.apps.get_model('tender', 'FinancialRatio').objects.filter(
                section_id=obj.id, supplier_id=self.context['supplier_id']
            ).first()
            return TenderFinancialRatioSerializer(ratios, many=False).data
        else:
            return None


class TenderFinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('tender', 'FinancialRatio')
        fields = [
            "id", "equity", "curr_liabilities", "debtors", "turnover", "gross_profit", "net_profit",
            "cash", "fixed_assets", "current_assets"
        ]


class TenderQuestionPreviewSerializer(serializers.ModelSerializer):
    response = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model("tender", "Question")
        fields = [
            "id", "description", "answer_type",
            "trans_description", "response",
        ]

    def get_response(self, obj):
        supplier_id = self.context['supplier_id']
        response = (
            apps.apps.get_model("tender", "SupplierResponse")
            .objects.filter(supplier_id=supplier_id, question_id=obj.id)
            .first()
        )
        return TenderSupplierResponse(response, many=False).data


class EmptySerializer(serializers.Serializer):
    class Meta:
        fields = []


class SupplierProfileSelectionBidSerializer(serializers.Serializer):
    file_type = serializers.CharField(max_length=100)
    class Meta:
        fields = ['file_type']


class SupplierFinancialResponseCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model("tender", "SupplierFinancialResponse")
        fields = [
            'id', 'supplier', 'category', 'awarded', 'excel_url'
        ]
        ref_name = "TenderSupplierFinancialResponseSerializer"