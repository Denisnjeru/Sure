from django.db import models
from apps.core.models import BaseModel
from apps.prequal.models import Category
from apps.suppliers.models import Supplier
from apps.buyer.models import Buyer
from apps.authentication.models import User

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

class CategorySupplier(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category Supplier"
        verbose_name_plural = "Category Suppliers"

    def __str__(self):
        return self.supplier.company_name + " - " + self.category.name

class ContractSection(BaseModel):
    name = models.CharField(max_length=250)
    content = models.TextField(blank=False, null=True)
    created_by = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Contract Section"
        verbose_name_plural = "Contract Sections"

class ContractTemplate(BaseModel):
    name = models.CharField(max_length=250)
    content = models.TextField(blank=False, null=True)
    created_by = models.ForeignKey(
        User, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Contract Template"
        verbose_name_plural = "Contract Templates"

class SupplierContract(BaseModel):
    APPROVAL_STATUS = (
        ("PENDING", ("Pending")),
        ("COMPLETED", ("Completed")),
        ("PROGRESS", ("In Progress")),
    )
    CONTRACT_STATUS = (
        ("PENDING", ("Pending")),
        ("ACTIVE", ("Active")),
        ("EXPIRED", ("Expired")),
    )

    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    contact_emails = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField(blank=True, null=True)
    status = models.CharField(
        choices=CONTRACT_STATUS, default="Pending", max_length=200
    )
    live_edit = models.BooleanField(default=False)
    live_editor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="live_editor"
    )
    approval_status = models.CharField(
        choices=APPROVAL_STATUS, default="Pending", max_length=200
    )
    created_by = models.ForeignKey(
        Buyer, blank=True, null=True, on_delete=models.SET_NULL
    )

    class Meta:
        verbose_name = "Supplier Contract"
        verbose_name_plural = "Supplier Contracts"

    def __str__(self):
        return self.supplier.company_name + " - " + str(self.category)

class Contract(BaseModel):
    APPROVAL_STATUS = (
        ("PENDING", ("Pending")),
        ("COMPLETED", ("Completed")),
        ("PROGRESS", ("In Progress")),
    )
    CONTRACT_STATUS = (
        ("PENDING", ("Pending")),
        ("ACTIVE", ("Active")),
        ("EXPIRED", ("Expired")),
    )

    # entity can be buyer or supplier
    contract_with = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="contract_with")
    entity_id = models.IntegerField()
    entity_object = GenericForeignKey('contract_with', 'entity_id')
    # contract for category/job
    contract_for = models.ForeignKey(ContentType, on_delete=models.CASCADE, related_name="contract_for")
    target_id = models.IntegerField()
    target_object = GenericForeignKey('contract_for', 'target_id')
    contact_emails = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    content = models.TextField(blank=True, null=True)
    document = models.FileField(blank=True, null=True, upload_to='uploads/contracts/')
    live_edit = models.BooleanField(default=False)
    live_editor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="contract_live_editor"
    )
    status = models.CharField(
        choices=CONTRACT_STATUS, default="Pending", max_length=200
    )
    approval_status = models.CharField(
        choices=APPROVAL_STATUS, default="Pending", max_length=200
    )
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL,
        related_name="contract_created_by"
    )

    class Meta:
        verbose_name = "Contract"
        verbose_name_plural = "Contracts"
        ordering = ('-id',)

    def __str__(self):
        return str(self.contract_with) + " - " + str(self.entity_id) + " - " + str(self.contract_for)  + " - " + str(self.target_id)


class ContractDocument(BaseModel):
    contract = models.ForeignKey(
        SupplierContract, blank=False, null=False, on_delete=models.CASCADE
    )
    priority = models.IntegerField()
    contract_section = models.ForeignKey(
        ContractSection, blank=False, null=False, on_delete=models.CASCADE
    )


class SupplierContractRevisions(BaseModel):
    contract = models.ForeignKey(
        SupplierContract, blank=False, null=False, on_delete=models.CASCADE
    )
    editor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    live_edit = models.BooleanField(default=False)
    content = models.TextField(blank=False, null=True)

class ContractRevisions(BaseModel):
    contract = models.ForeignKey(
        Contract, blank=False, null=False, on_delete=models.CASCADE
    )
    editor = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL
    )
    live_edit = models.BooleanField(default=False)
    document = models.FileField(blank=True, null=True, upload_to='uploads/contracts/revisions/')
    changes = models.FileField(blank=True, null=True, upload_to='uploads/contracts/revisions/changes')
    content = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Contract Revision"
        verbose_name_plural = "Contract Revisions"
        ordering = ('-id',)

# class ContractSectionCategoryType(BaseModel):
#     contract_section = models.ForeignKey(
#         ContractSection, blank=False, null=False, on_delete=models.CASCADE
#     )
#     category_type = models.ForeignKey(
#         CategoryType, blank=False, null=False, on_delete=models.CASCADE
#     )
#
#
# class ContractDocument(BaseModel):
#     contract = models.ForeignKey(
#         Contract, blank=False, null=False, on_delete=models.CASCADE
#     )
#     contract_contract_sections = models.TextField()
#
#     class Meta:
#         verbose_name = "Contract Document"
#         verbose_name_plural = "Contract Documents"
