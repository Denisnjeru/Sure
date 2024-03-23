from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from jmespath import search

from .models import Company, Buyer, BuyerRole, BuyerPrivilege, BuyerRolePrivilege


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = [
        "company_name",
        "phone_number",
        "contact_name",
        "kra_pin_number",
    ]
    list_filter = [
        "company_name",
    ]
    search_fields = [
        "company_name",
    ]


@admin.register(BuyerRole)
class BuyerRoleAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "description",
    ]
    list_filter = ["name"]

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "first_name",
    ]
    list_filter = ["company"]

admin.site.register(BuyerPrivilege)
admin.site.register(BuyerRolePrivilege)
