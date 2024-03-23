from django.contrib import admin
from .models import (
    Supplier,
    SupplierCompany,
    SupplierCompanyUser,
    SupplierPrivilege,
    SupplierRole,
    SupplierCompanyProfile,
    SupplierRolePrivilege
)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "short_name",
        "phone_number",
        "contact_name",
        "country",
        "location",
    ]
    list_filter = [
        "country",
        "location",
    ]
    search_fields = [
        "company_name",
        "kra_pin_number",
    ]


@admin.register(SupplierCompany)
class SupplierCompanyAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "tax_pin_number",
        "phone_number",
        "contact_name",
        "country",
    ]

    list_filter = [
        "country",
    ]


@admin.register(SupplierRole)
class SupplierRoleAdmin(admin.ModelAdmin):
    list_display = ["name", "description"]


@admin.register(SupplierPrivilege)
class SupplierRoleAdmin(admin.ModelAdmin):
    list_display = ["title", "description"]

@admin.register(SupplierRolePrivilege)
class SupplierRolePrivilegeAdmin(admin.ModelAdmin):
    list_display = ["supplier_role", "supplier_privilege"]

@admin.register(SupplierCompanyUser)
class SupplierCompanyUserAdmin(admin.ModelAdmin):
    list_display = ["supplier_name", "supplier_email", "supplier_role"]

@admin.register(SupplierCompanyProfile)
class SupplierCompanyProfileAdmin(admin.ModelAdmin):
    list_display = ["supplier_company"]
