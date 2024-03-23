from pyexpat import model
from tabnanny import verbose
import os
from django import apps
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from apps.authentication.models import User
from apps.common.models import country_choices, location_choices
from apps.core.models import BaseModel
from apps.core.utils import show
from backend.storage_backends import PrivateMediaStorage


class SupplierCompany(BaseModel):
    """
    Supplier Company, multiple supplier accounts
    """

    company_name = models.CharField(max_length=256)
    tax_pin_number = models.CharField(_("tax pin"), max_length=256, unique=True)
    phone_number = models.CharField(_("phone number"), max_length=100)
    contact_name = models.CharField(_("contact name"), max_length=200)
    country = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Supplier Company"
        verbose_name_plural = "Supplier Companies"

    def __str__(self):
        return self.company_name


class SupplierRole(BaseModel):
    """
    Supplier Roles
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    company = models.ForeignKey(SupplierCompany, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Supplier Role"
        verbose_name_plural = "Supplier Roles"

    def __str__(self):
        return self.name

def get_image_path(instance, filename):
    return os.path.join("images", str(instance.id), filename)


class Supplier(User):
    """
    Suppliers Model
    """
    LIMITED = 1
    SOLE = 2
    PARTNERSHIP = 3

    SUPPLIER_TYPE = (
        (LIMITED, "Limited"),
        (SOLE, "Sole Proprietor"),
        (PARTNERSHIP,"Partnership"),
    )

    company_name = models.CharField(_("company name"), max_length=200, db_index=True)
    short_name = models.CharField(
        _("short name"), max_length=200, null=True, blank=True
    )
    phone_number = models.CharField(_("phone number"), max_length=100)
    contact_name = models.CharField(_("contact name"), max_length=200)
    kra_pin_number = models.CharField(
        _("tax pin"), max_length=200, blank=True, null=True, unique=True
    )
    password_date = models.DateTimeField(
        _("password date"), auto_now_add=True, db_index=True
    )
    country = models.CharField(
        _("country"), max_length=200, choices=country_choices(), null=True, blank=True,
    )
    location = models.CharField(
        _("location"), max_length=200, choices=location_choices(), blank=True, null=True
    )
    address = models.CharField(_("address"), max_length=256, null=True, blank=True)
    unsubscribe = models.BooleanField(default=False, blank=True, null=True)
    logo_url = models.ImageField(
        upload_to=get_image_path,
        validators=[FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg"])],
        # storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )
    supplier_role = models.ForeignKey(
        SupplierRole, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    supplier_company = models.ForeignKey(
        SupplierCompany, on_delete=models.DO_NOTHING, blank=True, null=True
    )
    supplier_type= models.CharField(max_length=100, choices=SUPPLIER_TYPE, default=LIMITED)

    class Meta:
        verbose_name = "Supplier"
        verbose_name_plural = "Suppliers"

    def __str__(self):
        return self.contact_name

    @property
    def email_address(self):
        return self.get_username()

    @property
    def profile(self):
        p = SupplierCompanyProfile.objects.filter(supplier_company_id=self.supplier_company_id).first()
        return p
    # def prequal_question_response(self, question):
    #     response = "No response submitted"
    #     if question is not None:
    #         supplier_response = (
    #             apps.apps.get_model("prequal", "SupplierResponse")
    #             .objects.filter(question_id=question.id, supplier_id=self.id)
    #             .first()
    #         )
    #         if supplier_response is not None and supplier_response.response != "":
    #             response = supplier_response.response
    #     return response

    def total_prequal_score(self, category_id):
        category_score = (
            apps.apps.get_model("prequal", "SupplierCategoryScore")
            .objects.filter(category_id=category_id)
            .first()
        )
        if category_score:
            return category_score.score
        else:
            return 0

    def total_tender_score(self, category_id):
        category_score = (
            apps.apps.get_model("tender", "SupplierTechnicalScore")
            .objects.filter(category_id=category_id)
            .first()
        )
        if category_score:
            return category_score.score
        else:
            return 0

    def score_rank(self, category_id):
        category_score = (
            apps.apps.get_model("prequal", "SupplierCategoryScore")
            .objects.filter(category_id=category_id, supplier_id=self.id)
            .first()
        )
        if category_score:
            return category_score.rank
        else:
            return ""

    def tender_category_rank(self, category):
        category_score = apps.apps.get_model("tender", "SupplierCategoryScore").objects.filter(
            supplier_id=self.id, category_id=category.id
        ).first()
        if category_score is not None and category_score.rank is not None:
            return category_score.rank
        # category.refresh_scores()
        return 0

    def tender_technical_score_rank(self, category_id):
        category_score = (
            apps.apps.get_model("tender", "SupplierTechnicalScore")
            .objects.filter(category_id=category_id, supplier_id=self.id)
            .first()
        )
        if category_score:
            return category_score.rank
        else:
            return ""

    def prequal_section_score(self, section_id):
        section_score = (
            apps.apps.get_model("prequal", "SupplierSectionScore")
            .objects.filter(section_id=section_id, supplier_id=self.id)
            .first()
        )
        if section_score:
            return section_score.score
        else:
            return 0

    def tender_section_score(self, section_id):
        section_score = (
            apps.apps.get_model("tender", "SupplierSectionScore")
            .objects.filter(section_id=section_id, supplier_id=self.id)
            .first()
        )
        if section_score:
            return section_score.score
        else:
            return 0

    def prequal_question_response(self, question_id):
        response = (
            apps.apps.get_model("prequal", "SupplierResponse")
            .objects.filter(supplier_id=self.id, question_id=question_id)
            .first()
        )
        if response:
            if response.options:
                return response.options
            elif response.document_url:
                return response.document_url.url
            else:
                return "N/R"
        else:
            return "N/R"

    def rfq_responses(self, category_id):
        responses = apps.apps.get_model("rfq", "RFQItemResponse").objects.filter(
            supplier_id=self.id, rfq_item__category_id=category_id
        )
        if responses.count() > 0:
            return responses
        return None

    def prequal_category_question_response(self, question):
        response = "No response submitted"
        if question is not None:
            supplier_response = (
                apps.apps.get_model("prequal", "SupplierResponse")
                .objects.filter(question_id=question.id, supplier_id=self.id)
                .first()
            )
            if supplier_response is not None and supplier_response.response != "":
                response = supplier_response.response
        return response

    def tender_category_question_response(self, question):
        response = "No response submitted"
        if question is not None:
            supplier_response = (
                apps.apps.get_model("tender", "SupplierResponse")
                .objects.filter(question_id=question.id, supplier_id=self.id)
                .first()
            )
            if supplier_response is not None and supplier_response.options != "":
                response = supplier_response.options
        return response

    def tender_question_response(self, question_id):
        response = (
            apps.apps.get_model("tender", "SupplierResponse")
            .objects.filter(supplier_id=self.id, question_id=question_id)
            .first()
        )
        if response:
            if response.options:
                return response.options
            elif response.document_url:
                return response.document_url.url
            else:
                return "N/R"
        else:
            return "N/R"

    def tender_total_item_weighted_score(self, item):
        tender = apps.apps.get_model('tender', 'Tender').objects.filter(id=item.category.tender_id).first()
        responses = apps.apps.get_model('tender', 'ItemResponse').objects.filter(item_id=item.id).order_by(
            "value"
        )
        if responses.count() > 2:
            lowest = None
            for response in responses:
                if float(show(response.total)) > item.outlier_score_final:
                    if lowest is not None:
                        if float(show(response.total)) < float(show(lowest.total)):
                            lowest = response
                        else:
                            lowest = lowest
                    else:
                        lowest = response

            if lowest:
                this_supplier = responses.filter(supplier_id=self.id).first()
                if this_supplier:
                    if float(show(this_supplier.total)) <= item.outlier_score_final:
                        return 0 + self.technical_weighted_score(category_id=item.category_id)
                    else:
                        weighted_score = (
                            float(show(lowest.total)) / float(show(this_supplier.total))
                        ) * float(tender.financial_weight)
                        return weighted_score + float(
                            self.tender_technical_weighted_score(category_id=item.category_id)
                        )
                else:
                    return 0 + float(self.tender_technical_weighted_score(category_id=item.category_id))
            else:
                return 0 + float(self.tender_technical_weighted_score(category_id=item.category_id))
        else:
            lowest = responses.first()
            this_supplier = responses.filter(supplier_id=self.id).first()
            if lowest:
                if this_supplier:
                    weighted_score = (
                        float(show(lowest.total)) / float(show(this_supplier.total))
                    ) * float(tender.financial_weight)
                    return weighted_score + self.tender_technical_weighted_score(category_id=item.category_id)
                else:
                    return 0 + float(self.tender_technical_weighted_score(category_id=item.category_id))
            else:
                return 0 + float(self.tender_technical_weighted_score(category_id=item.category_id))

    def tender_technical_weighted_score(self, category_id):
        score = apps.apps.get_model('tender', 'SupplierTechnicalScore').objects.filter(
            category_id=category_id, supplier_id=self.id
        ).first()
        if score:
            return score.weighted_score
        return 0

    def tender_item_weighted_score(self, item):
        tender = apps.apps.get_model('tender', 'Tender').objects.filter(id=item.category.tender_id).first()
        if tender:
            responses = apps.apps.get_model('tender', 'ItemResponse').objects.filter(item_id=item.id).order_by(
                "value"
            )
            if responses.count() > 2:
                lowest = None
                for response in responses:
                    if float(show(response.total)) > item.outlier_score_final:
                        if lowest is not None:
                            if float(show(response.total)) < float(show(lowest.total)):
                                lowest = response
                            else:
                                lowest = lowest
                        else:
                            lowest = response

                if lowest:
                    this_supplier = responses.filter(supplier_id=self.id).first()
                    if this_supplier:
                        if float(show(this_supplier.total)) <= item.outlier_score_final:
                            return f"O_{0}"
                        else:
                            weighted_score = (
                                float(show(lowest.total)) / float(show(this_supplier.total))
                            ) * float(tender.financial_weight)
                            return f"Tc_{weighted_score}"
                    else:
                        return f"Ac_N/A"
                else:
                    return f"O_{0}"
            else:
                lowest = responses.first()
                this_supplier = responses.filter(supplier_id=self.id).first()
                if lowest:
                    if this_supplier:
                        try:
                            weighted_score = (
                                float(show(lowest.total)) / float(show(this_supplier.total))
                            ) * float(tender.financial_weight)
                        except:
                            weighted_score = 0

                        return f"Tc_{weighted_score}"
                    else:
                        return f"Ac_N/A"
                else:
                    return f"Ac_N/A"
        else:
            return "Ac_N/A"

    def tender_question_score(self, question):
        """works out how much a supplier scored in a question base on response"""
        # todo refine
        from apps.suppliers.utils import tender_financial_ratio_question_score

        score = 0
        if question.is_scored:
            question_response = apps.apps.get_model("tender", "SupplierResponse").objects.filter(
                supplier_id=self.id, question_id=question.id).first()
            if (
                question_response is not None
                and question_response.options is not None
                and len(question_response.options) > 0
            ):
                if question.section.name == "Financial Ratios":
                    score = tender_financial_ratio_question_score(
                        supplier=self, question=question
                    )
                if question.answer_type == apps.apps.get_model("tender", "Question").TYPE_UPLOAD:
                    score = float(question.max_score)
                if question_response.options in question.options:
                    response_index = question.options.index(question_response.options)
                    score = float(question.scores[response_index])
                if question_response.options == "True":
                    score = float(question.max_score)
        return score

    def prequal_question_score(self, question):
        """works out how much a supplier scored in a question base on response"""
        # todo refine
        from apps.suppliers.utils import prequal_financial_ratio_question_score

        score = 0
        if question.is_scored:
            question_response = apps.apps.get_model("prequal", "SupplierResponse").objects.filter(
                supplier_id=self.id, question_id=question.id).first()
            if (
                question_response is not None
                and question_response.options is not None
                and len(question_response.options) > 0
            ):
                if question.section.name == "Financial Ratios":
                    score = prequal_financial_ratio_question_score(
                        supplier=self, question=question
                    )
                if question.answer_type == apps.apps.get_model("prequal", "Question").TYPE_UPLOAD:
                    score = float(question.max_score)
                if question_response.options in question.options:
                    response_index = question.options.index(question_response.options)
                    score = float(question.scores[response_index])
                if question_response.options == "True":
                    score = float(question.max_score)
        return score

    # def prequal_section_score(self, section):
    #     total_score = 0
    #     if section is not None:
    #         section_score = apps.apps.get_model('prequal', 'SupplierSectionScore').objects.filter(
    #             supplier_id=self.id, section_id=section.id
    #         ).first()
    #         if section_score is None:
    #             for question in list(set(section.questions)):
    #                 total_score += self.prequal_question_score(question)
    #             self.resolve_section_score(section, total_score)
    #         else:
    #             total_score = section_score.score
    #     return total_score


class SupplierPrivilege(BaseModel):
    """
    Supplier Privileges
    """

    privilege_codes = {
        "MANAGE_USER": "Managing users",
        "MANAGE_TENDER": "Tender management",
        "MANAGE_RFQ": "RFQ management",
        "MANAGE_PREQUAL": "Prequal management",
        "MANAGE_ASSET_DISPOSAL": "Asset Disposal management",
        "VIEW_REPORT": "Reports",
        "MAKE_PAYMENTS": "Make Payments",
        "UPDATE_COMPANY_INFO": "Profile Management",
    }
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Supplier Privilege"
        verbose_name_plural = "Supplier Privileges"

    def __str__(self):
        return self.title


class SupplierRolePrivilege(BaseModel):
    supplier_role = models.ForeignKey(
        SupplierRole,
        related_name="supplier_role",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    supplier_privilege = models.ForeignKey(
        SupplierPrivilege,
        related_name="supplier_role_privilege",
        on_delete=models.CASCADE,
        blank=False,
    )

    class Meta:
        verbose_name = "Supplier Role Privilege"
        verbose_name_plural = "Supplier Role Privieges"


class SupplierCompanyUser(User):
    supplier_company = models.ForeignKey(SupplierCompany, on_delete=models.CASCADE)
    supplier_name = models.CharField(max_length=256)
    supplier_email = models.EmailField(max_length=50)
    supplier_role = models.ForeignKey(SupplierRole, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Supplier Company User"
        verbose_name_plural = "Supplier Company Users"

    def __str__(self):
        return self.supplier_name


class SupplierCompanyProfile(BaseModel):
    """
    Supplier's Company Profile
    """

    validators = [
        FileExtensionValidator(
            allowed_extensions=[
                "pdf",
                "doc",
                "jpg",
                "png",
                "jpeg",
            ]
        )
    ]

    supplier_company = models.ForeignKey(
        SupplierCompany,
        on_delete=models.CASCADE,
    )
    registration_cert_url = models.FileField(
        upload_to="supplier_documennts",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    logo_url = models.ImageField(
        upload_to="supplier_logos/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
    )
    kra_pin_url = models.FileField(
        upload_to="supplier_documents/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    kra_compliance_url = models.FileField(
        upload_to="supplier_documents/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    kra_trading_licence_url = models.FileField(
        upload_to="supplier_documents/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    cr_12_document_url = models.FileField(
        upload_to="supplier_documents/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    kra_compliance_expiry_date = models.DateField(
        blank=True,
        null=True,
    )
    kra_trading_licence_expiry_date = models.DateField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "Supplier Profile"
        verbose_name_plural = "Supplier Profiles"

    def __str__(self):
        return self.supplier_company.company_name
