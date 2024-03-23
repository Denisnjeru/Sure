from django.contrib import admin

from apps.rfq.models import (
    RFQCategoryReport,
    RFQItem,
    RFQJobReport,
    Rfq,
    Category,
    RfqInvitee,
    RFQItemResponse,
    SupplierResponse,
    SupplierRfqTotal,
)


@admin.register(Rfq)
class RfqAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "title",
        "unique_reference",
        "status",
    ]
    list_filter = [
        "company",
        "status",
    ]
    search_fields = [
        "title",
    ]


@admin.register(Category)
class CategoryRfqAdmin(admin.ModelAdmin):
    list_display = [
        "rfq",
        "name",
        "unique_reference",
        "opening_date",
        "closing_date",
        "currency",
    ]
    list_filter = [
        "rfq",
    ]
    search_fields = [
        "name",
        "unique_reference",
    ]


@admin.register(RFQItem)
class RFQItemAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "item_description",
        "item_number",
        "quantity",
    ]
    list_filter = [
        "category",
    ]
    search_fields = [
        "category",
    ]


@admin.register(RfqInvitee)
class RFQInviteeAdmin(admin.ModelAdmin):
    list_display = ["category", "supplier", "email"]
    list_filter = [
        "category",
    ]
    search_fields = [
        "category",
    ]


@admin.register(RFQItemResponse)
class RFQItemResponseAdmin(admin.ModelAdmin):
    list_display = [
        "supplier",
        "rfq_item",
        "unit_price",
        "total_price",
    ]


@admin.register(SupplierResponse)
class SupplierResponseAdmin(admin.ModelAdmin):
    list_display = ["supplier", "category", "document_url"]


@admin.register(SupplierRfqTotal)
class SupplierRfqTotalAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "supplier",
        "score",
        "has_outlier",
        "has_blank",
    ]


@admin.register(RFQCategoryReport)
class RFQCategoryReportAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "category_rfq_pdf",
        "financial",
    ]


@admin.register(RFQJobReport)
class RFQJobReportAdmin(admin.ModelAdmin):
    list_display = [
        "job",
        "job_savings",
        "participation_report",
        "job_lowest_item_cost",
    ]
