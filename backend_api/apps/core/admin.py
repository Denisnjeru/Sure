from django.contrib import admin
from .models import (
    CategoryTypeSupplier, EmailOut, Notifications, SupplierReceipt, CategoryTypeSupplierLocation, Job, CategoryGroup, CategoryType, Currency, Country, CategoryOrder, Payment,CategoryOrder, Payment, CategoryTypeSupplier, CriteriaCountry,CategoryTypeCriteria, \
    CurrentSupplier
)

# Register your models here.
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "sourcing_activity",
        "target_id",
    ]
    list_filter = [
        "company__company_name",
        "sourcing_activity",
        "target_id",
    ]
    search_fields = [
        "company",
        "sourcing_activity",
    ]

@admin.register(CategoryGroup)
class CategoryGroupAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "code",
    ]

@admin.register(CategoryType)
class CategoryTypeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "innitials",
    ]

@admin.register(CategoryTypeSupplier)
class CategoryTypeSupplierAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "primary_email",
        "category_type"
    ]

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "initials",
    ]

@admin.register(CategoryOrder)
class CategoryOrderAdmin(admin.ModelAdmin):
    list_display = [
        "target", "category_id", "supplier", "code", "payment_status"
    ]

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        "model", "instance_id", "timestamps"
    ]

@admin.register(CategoryTypeSupplierLocation)
class CategoryTypeSupplierLocationAdmin(admin.ModelAdmin):
    list_display = [
        "category_type_supplier","location"
    ]

@admin.register(CurrentSupplier)
class CurrentSupplierAdmin(admin.ModelAdmin):
    list_display = [
        "company", "target", "category_id", "supplier_name", "supplier_email", "supplier_phone"
    ]


@admin.register(EmailOut)
class EmailOutAdmin(admin.ModelAdmin):
    list_display = [
        "subject", "to", "body", "message", "target", "category_id", "type", "sent", "error"
    ]
    
# @admin.register(Notifications)
# class NotificationsAdmin(admin.ModelAdmin):
#     list_display = [
#         "company", "target", "category_id", "supplier_name", "supplier_email", "supplier_phone"
#     ]

admin.site.register(Country)
admin.site.register(CriteriaCountry)
admin.site.register(CategoryTypeCriteria)
admin.site.register(SupplierReceipt)


