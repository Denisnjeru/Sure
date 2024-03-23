from django.contrib import admin
from .models import (
    CategorySupplier, ContractSection, SupplierContract, ContractTemplate, Contract, ContractRevisions
)

# Register your models here.
@admin.register(CategorySupplier)
class CategorySupplierAdmin(admin.ModelAdmin):
    list_display = [
        "category",
        "supplier",
    ]

@admin.register(ContractSection)
class ContractSectionAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_by",
        "created_at",
        "updated_at"
    ]

@admin.register(ContractTemplate)
class ContractTemplateAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "created_by",
        "created_at",
        "updated_at"
    ]

@admin.register(SupplierContract)
class SupplierContractAdmin(admin.ModelAdmin):
    list_display = [
        "supplier",
        "created_by",
        "created_at",
        "updated_at"
    ]

@admin.register(ContractRevisions)
class ContractRevisionsAdmin(admin.ModelAdmin):
    list_display = [
        "contract",
        "editor",
        "live_edit"
    ]

@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = [
        "contract_with",
        "entity_id",
        "contract_for",
        "target_id",
        "created_at",
        "updated_at"
    ]
