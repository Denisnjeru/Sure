from tabnanny import verbose

from django import apps
from django.db import models
from django.core.validators import FileExtensionValidator
from apps.authentication.models import User

from apps.common.models import country_choices
from apps.core.models import BaseModel
from backend.storage_backends import PrivateMediaStorage


class Company(BaseModel):
    """
    Companies signed up with Tendersure
    """

    company_name = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256, unique=True)
    contact_name = models.CharField(max_length=100)
    country = models.CharField(
        max_length=50, choices=country_choices(), null=True, blank=True
    )
    buyer_initials = models.CharField(max_length=20)
    kra_pin_number = models.CharField(max_length=50)
    company_logo_url = models.FileField(
        upload_to="",
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.company_name

    @property
    def has_open_jobs(self):
        prequals = apps.apps.get_model('prequal', 'Category').objects.filter(
            prequalification__company_id=self.id
        )
        tenders = apps.apps.get_model('tender', 'Category').objects.filter(
            tender__company_id=self.id
        )
        if prequals.count() > 0 or tenders.count() > 0:
            return True
        else:
            return False


class BuyerRole(BaseModel):
    """
    Buyer Roles
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Buyer Role"
        verbose_name_plural = "Buyer Roles"

    def __str__(self) -> str:
        return self.name


class BuyerPrivilege(BaseModel):
    """
    Buyer Privileges
    """

    privilege_codes = {
        "MANAGE_USER": "Managing users",
        "MANAGE_JOB": "Job management",
        "VIEW_REPORT": "Reports",
        "MANAGE_CATEGORY": "Categories managements",
        "SEND_PARTICIPANT_LIST": "Participant communications",
        "UPDATE_COMPANY_INFO": "Profile Management",
        "VIEW_SUPPLIER_FILES": "Supplier information",
        "BLACKLIST_SUPPLIER": "Supplier management",
        "CREATE_DOCUMENTS": "Document Management",
        "EDIT_COMPANY": "Company Details",
    }
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Buyer Privilege"
        verbose_name_plural = "Buyer Privileges"


class BuyerRolePrivilege(BaseModel):
    buyer_role = models.ForeignKey(
        BuyerRole,
        related_name="buyer_role",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    buyer_privilege = models.ForeignKey(
        BuyerPrivilege,
        related_name="buyere_role_privilege",
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = "Buyer Role Privilege"
        verbose_name_plural = "Buyer Role Privieges"
        unique_together = (('buyer_role', 'buyer_privilege',),)


class Buyer(User):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="buyers"
    )
    buyer_role = models.ForeignKey(
        BuyerRole,
        on_delete=models.CASCADE,
    )
    password_date = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "Company User"
        verbose_name_plural = "Company Users"
