from email.policy import default
from multiprocessing import context
import traceback

from django.apps import apps
from numpy import source
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from apps.rfq.models import *
from apps.core.models import CategoryType
from apps.buyer import serializers as buyer_serializers


class JobListSerializer(serializers.ModelSerializer):
    approved_by = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    company = buyer_serializers.CompanyListSerializer(many=False)

    class Meta:
        model = Rfq
        fields = [
            "id",
            "title",
            "unique_reference",
            "status",
            "approved_by",
            "created_by",
            "is_open",
            "company",
        ]
        ref_name = "RFQJobListSerializer"

    def get_approved_by(self, obj):
        if obj.approved_by:
            return f"{obj.approved_by.first_name} {obj.approved_by.last_name}"
        else:
            return ""

    def get_is_open(self, obj):
        if Category.objects.filter(status_open=True, rfq_id=obj.id).count() > 0:
            return True
        else:
            return False


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rfq
        fields = [
            "id",
            "company",
            "title",
            "unique_reference",
            "created_by",
            "show_bids",
        ]
        ref_name = "RFQJobCreateUpdateSerializer"


class RFQCatSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rfq
        fields = [
            'category_suppliers',
        ]


class RfqCategorySerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    job = serializers.CharField(read_only=True, source="rfq.title")
    job_name = serializers.CharField(read_only=True, source="rfq.title")
    job_type = serializers.SerializerMethodField()
    company_name = serializers.CharField(
        read_only=True, source="rfq.company.company_name"
    )

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "unique_reference",
            "opening_date",
            "closing_date",
            "evaluation_date",
            "unique_reference",
            "status_open",
            "invite_notification",
            "instructions",
            "self_evaluate",
            "job",
            "job_name",
            "job_type",
            "participants",
            "company_name",
        ]

    def get_opening_date(self, obj):
        return obj.opening_date

    def get_closing_date(self, obj):
        return obj.closing_date

    def get_participants(self, obj):
        s = apps.get_model("suppliers", "Supplier").objects.filter(
            id__in=RFQItemResponse.objects.filter(rfq_item__category_id=obj.id).only("supplier_id").values("supplier_id").distinct()
        )
        # s = RFQItemResponse.objects.filter(rfq_item__category_id=obj.id).distinct("supplier").count()
        return s.count()

    def get_job_type(self, obj):
        return 'RFQ'


class RfqCategoryRetrieveSerializer(serializers.ModelSerializer):
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()
    items = serializers.SerializerMethodField()
    rfq = JobListSerializer(many=False)
    items_template = serializers.SerializerMethodField()
    supplier_participation_status = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "opening_date",
            "closing_date",
            "evaluation_date",
            "unique_reference",
            "status_open",
            "invite_notification",
            "instructions",
            "self_evaluate",
            "rfq",
            "items",
            "currency",
            "rfq_type",
            "vatable",
            "vat_rate",
            "items_template",
            "supplier_participation_status",
        ]

    def get_opening_date(self, obj):
        #return obj.opening_date.strftime("%Y-%m-%d %H:%M:%S")
        return obj.opening_date

    def get_closing_date(self, obj):
        #return obj.closing_date.strftime("%Y-%m-%d %H:%M:%S")
        return obj.closing_date
        
    def get_items(self, obj):
        items = RFQItem.objects.filter(category_id=obj.id).order_by("item_number")
        s = RfqItemSerializer(items, many=True, context=self.context)
        return s.data

    def get_currency(self, obj):
        return obj.currency.initials

    def get_items_template(self, obj):
        return obj.items_template.url
    
    def get_supplier_participation_status(self,obj):
        supplier_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.get_model("suppliers", "Supplier")
            .objects.filter(id=supplier_id)
            .first()
        )
        if supplier is not None:
            sup_responses = RFQItemResponse.objects.filter(rfq_item__category_id=obj.id).values_list("supplier", flat=True)
 
            if supplier.id in sup_responses:
                return True
            else:
                return False
        else:
            return False


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("core", "Currency")
        fields = ["id", "name", "initials"]


class RfqCategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = ["id", "name", "category_group", "innitials"]


class RfqCategoryCreateSerializer(serializers.ModelSerializer):
    items_template = serializers.FileField()

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "rfq",
            "category_type",
            "opening_date",
            "closing_date",
            "unique_reference",
            "evaluation_date",
            "invite_notification",
            "instructions",
            "self_evaluate",
            "items_template",
            "currency",
            "rfq_type",
            "vatable",
            "vat_rate",
        ]


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("suppliers", "Supplier")
        fields = (
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
        )


class RfqItemSerializer(serializers.ModelSerializer):
    item_responses = serializers.SerializerMethodField()

    class Meta:
        model = RFQItem
        fields = [
            "id",
            "item_description",
            "unit_of_measure",
            "item_number",
            "current_price",
            "quantity",
            "item_code",
            "specification_1",
            "specification_2",
            "item_responses",
        ]

    def get_item_responses(self, obj):
        supplier_id = self.context["request"].auth.payload["user_id"]
        supplier = (
            apps.get_model("suppliers", "Supplier")
            .objects.filter(id=supplier_id)
            .first()
        )
        if supplier is not None:
            responses = RFQItemResponse.objects.filter(
                supplier_id=supplier_id, rfq_item=obj
            ).order_by("id")
            s = RfqItemResponseSerializer(responses, many=True)
            return s.data
        else:
            return []


class RfqItemCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem

        fields = [
            "id",
            "item_description",
            "item_number",
            "current_price",
            "quantity",
            "item_code",
        ]
        read_only_fields = ("id",)


class RfqItemRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItem

        fields = [
            "id",
            "item_description",
            "item_number",
            "current_price",
            "quantity",
            "item_code",
        ]
        read_only_fields = ("id",)


class RfqSupplierResponseSerializer(serializers.ModelSerializer):
    item_responses = serializers.SerializerMethodField()

    class Meta:
        model = SupplierResponse
        fields = ["id", "supplier", "category", "document_url", "item_responses"]

    def get_item_responses(self, obj):
        supplier_id = self.context["request"].auth.payload["user_id"]
        responses = RFQItemResponse.objects.filter(
            supplier_id=supplier_id, rfq_item__category_id=obj.category_id
        ).order_by("id")
        print(responses)
        s = RfqItemResponseSerializer(responses, many=True)
        return s.data


class RfqItemResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFQItemResponse
        fields = [
            "id",
            "supplier",
            "unit_price",
            "total_price",
            "cell_data",
            "column_data",
            "item_number",
        ]


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model("suppliers", "Supplier")
        fields = ["id", "company_name", "contact_name", "phone_number"]


# class ParticipantSerializer(serializers.ModelSerializer):
#     supplier = supplier_serializers.SupplierListSerializer(many=False)
#     total = serializers.SerializerMethodField()


#     class Meta:
#         model = SupplierResponse
#         fields = ["id", "category","supplier","total"]

# def get_rank(self, obj):
#     if not obj.category.status_open:
#         total = SupplierRfqTotal.objects.filter(supplier_id=obj.supplier_id).first()
#         if total is not None:
#             return total.rank
#         else:
#             return "Not Evaluated"
#     else:
#         return "Rfq Is Still Open!!"

# def get_total(self, obj):
#     if not obj.category.status_open:
#         total = SupplierRfqTotal.objects.filter(supplier_id=obj.supplier_id).first()
#         if total is not None:
#             return total.score
#         else:
#             return "Not Evaluated"
#     else:
#         return "Rfq Is Still Open!!"


class SupplierInviteeSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=5000)

    class Meta:
        model = RfqInvitee
        fields = ["email", "category"]


class InvitedSupplierSerializer(serializers.ModelSerializer):
    category = RfqCategorySerializer(many=False)
    supplier = SupplierSerializer(many=False)

    class Meta:
        model = RfqInvitee
        fields = ["id", "category", "supplier", "email"]


class RfqOpenSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = Category
        fields = [
            "id",
            "closing_date",
        ]

    def create(self, validated_data):
        rfq_category = Category.objects.filter(id=validated_data["id"]).first()
        if not rfq_category.status_open:
            rfq_category.status_open = True
            rfq_category.closing_date = validated_data["closing_date"]
            rfq_category.save()
        return rfq_category


class SupplierRFQTotalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierRfqTotal
        fields = ["category", "supplier", "score", "has_outlier", "has_blank", "rank"]


class AdvancedRFQSerializer(serializers.Serializer):
    rfq_template = serializers.FileField()

    def validate(self, attrs):
        try:
            rfq_template = attrs["rfq_template"]
            # validate that rfq template end with xlsx
            if len(rfq_template) < 3:
                raise serializers.ValidationError("The file field cannot be empty", 401)

        except Exception as e:
            raise serializers.ValidationError(
                "The uploaded file must saved in the .xlsx format", 401
            )

        return super().validate(attrs)

class RFQExcelUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["current_prices_template",]

class RfqAdvancedSupplierResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierResponse
        fields = ["id", "supplier", "category", "document_url"]