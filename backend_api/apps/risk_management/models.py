import os
from pickle import TRUE
from django.db import models

# Create your models here.
import pgcrypto
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SlugField
from django.template.defaultfilters import slugify

from apps.core.models import BaseModel, CategoryType, Currency
from django.core.validators import FileExtensionValidator

from .utils import supplier_response_files
from apps.suppliers.models import Supplier
from backend.storage_backends import PrivateMediaStorage
from django.utils.translation import gettext_lazy as _


validators = [
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "png",
                    "jpeg",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ]

class RiskManagement(BaseModel):

    company = models.ForeignKey('buyer.Company', on_delete=models.CASCADE)
    title = models.CharField(_('Title'), max_length=1000, null=False, blank=False)
    unique_reference = models.CharField(max_length=1000)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='risk_approved_by', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='risk_created_by')
    send_participant_list_to_supplier = models.BooleanField(default=False)
    lang_en = models.BooleanField(default=False)
    # questions_template = models.FileField(
    #     upload_to="risk_management_qs/%Y/%m/%d", validators=validators,storage=PrivateMediaStorage(),
    #     blank=True, null=True, max_length=3000,
    # )
    questions_template = models.FileField(
        upload_to="risk_management_qs/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=3000,
    )

    class Meta:
        verbose_name = "RiskManagement"
        verbose_name_plural = "RiskManagement"
        ordering = ['created_at']

    # @property
    # def supporting_documents(self):
    #     documents = Supportingdocument.objects.filter(riskmanagement=self)
    #     return list(documents)

    # @property
    # def company(self):
    #     return self.category.job.company

    @property
    def first_section(self):
        return self.sections.filter(parent_section=None).first()

    @property
    def questions(self):
        return Question.objects.filter(section__category__riskmanagement=self)

    @property
    def required_questions(self):
        return Question.objects.filter(
            section__category__riskmanagement=self, is_required=True
        )

    @property
    def participants(self):
        suppliers = []
        questions = self.category.questions
        if questions:
            for question in questions:
                q_participants = question.participants
                for participant in q_participants:
                    if participant not in suppliers:
                        suppliers.append(participant)
                return set(suppliers)

        return None

    def count_participants(self):
        return len(self.participants)

    # @property
    # def invited_suppliers(self):
    #     suppliers = []
    #     invitees = CategoryInvitee.objects.filter(category=self.category)
    #     for invitation in invitees:
    #         suppliers.append(invitation.supplier)
    #     return list(set(suppliers))

    @property
    def sections(self):
        return Section.objects.filter(category__riskmanagement=self).order_by("id")

    @property
    def status(self):
        if self.has_open_category:
            return "Open"
        return "Closed"
    
    @property
    def approved(self):
        if self.approved_by:
            return True   
        return False

    @property
    def categories(self):
        return Category.objects.filter(riskmanagement=self).order_by(
            "unique_reference"
        )

    @property
    def has_open_category(self):
        for category in self.categories:
            if category.status_open == True:
                return True
        return False

class Category(BaseModel):
    name = models.CharField(max_length=1000)
    trans_name = models.CharField(max_length=1000, blank=True, null=True)
    unique_reference = models.CharField(max_length=1000)
    bid_charge = models.DecimalField(max_digits=20, decimal_places=2)
    pass_score = models.IntegerField(default=70)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    evaluation_date = models.DateTimeField(blank=True, null=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='risk_category_currency', blank=True, null=True)
    is_open = models.BooleanField(default=False)
    invite_only = models.BooleanField(default=False)
    allowed_staff = models.BooleanField(default=False)
    update_docs = models.BooleanField(default=False)
    send_participant_list_to_supplier = models.BooleanField(default=False)
    parent_category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True, null=True)
    riskmanagement = models.ForeignKey(RiskManagement, on_delete=models.CASCADE, related_name='risk_categories')
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name='risk_category_type',blank=True, null=True)
    # questions_template = models.FileField(
    #     upload_to="risk_management_qs/category/%Y/%m/%d", validators=validators,storage=PrivateMediaStorage(),
    #     blank=True, null=True, max_length=3000,
    # )
    questions_template = models.FileField(
        upload_to="risk_management_qs/category/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=3000,
    )

    class Meta:
        verbose_name = "Riskmanagement Category"
        verbose_name_plural = "Riskmanagement Categories"

    
    @property
    def sections(self):
        return Section.objects.filter(category=self).order_by("id")

    
    @property
    def questions(self):
        questions = []
        for section in self.sections:
            questions.extend(section.questions)
        return set(questions)

    @property
    def total_questions_count(self):
        questions = []
        for section in self.sections:
            questions.extend(section.questions)
        return len(questions)

    def scored_sections(self, sections=None):
        scored_sections = []
        if sections is None:
            sections = self.sections
        for section in sections:
            if section.is_scored:
                scored_sections.append(section)
        return scored_sections

    @property
    def participants(self):
        suppliers = []
        questions = self.questions
        if questions:
            for question in questions:
                q_participants = question.participants
                for participant in q_participants:
                    if participant not in suppliers:
                        suppliers.append(participant)
                return set(suppliers)

        return None
    @property
    def has_risk_assessment(self):
        if QualityAssurance.objects.filter(category=self).count() >= 1:
            return True
        else:
            return False

class QualityAssuranceManager(models.Manager):
    def has_qa_questions(self):
        questions = Question.objects.filter(is_qa=True, section=self)
        if questions.count() > 0:
            return True
        else:
            return False

class Section(BaseModel):
    name = models.CharField(max_length=200, db_index=True)
    trans_name = models.CharField(max_length=200, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent_section = models.ForeignKey(
        "Section", blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE, related_name='risk_sections'
    )
    name_slug = SlugField(blank=True, null=True)

    has_qa_q  = QualityAssuranceManager()
    objects = models.Manager()

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    @property
    def section_score(self):
        score = 0
        for question in self.questions:
            if question.is_scored:
                score += question.max_score
        return score

    @property
    def short_name_version(self):
        short_name = self.short_name
        if short_name is not None:
            return short_name
        return self.name

    @property
    def is_scored(self):
        for question in self.questions:
            if question.is_scored:
                return True
        return False

    @property
    def questions(self):
        questions = Question.objects.filter(section=self).order_by("id")
        return questions

    @property
    def document_questions(self):
        questions = Question.objects.filter(section=self, answer_type=5).order_by("id")
        return questions

    @property
    def has_child_sections(self):
        if Section.objects.filter(parent_section_id=self.id).count() > 0:
            return True
        else:
            return False

    @property
    def child_sections(self):
        return Section.objects.filter(parent_section=self).order_by("id")

    @property
    def parents(self):
        parents = []
        if self.parent_section is not None:
            parents.extend(self.parent_section.siblings)

        return list(set(parents))

    @property
    def parent(self):
        return self.parent_section

    @property
    def siblings(self):
        if self.parent_section is not None:
            return Section.objects.filter(parent_section=self.parent_section).order_by(
                "id"
            )  # todo check if should exclude self
        else:
            return Section.objects.filter(
                category=self.category, parent_section=None
            ).order_by("id")
        # return []

    @property
    def next_sibling(self):
        siblings = self.siblings
        for sibling in siblings:
            if sibling.id > self.id:
                return sibling
        return None

    def next_section(self, from_child=False):
        if not from_child:
            if self.child_sections.count() > 0:
                return self.child_sections.first()
            elif self.next_sibling:
                return self.next_sibling
            elif self.parent_section:
                return self.parent_section.next_section(from_child=True)
            return None
        else:
            if self.next_sibling:
                return self.next_sibling
            elif self.parent_section:
                return self.parent_section.next_section(from_child=True)
            return None

    @property
    def previous_section(self):

        if len(self.siblings) > 1:
            for sibling in self.siblings:
                if sibling.id < self.id:
                    return sibling
        else:
            return self.parent_section.previous_section

    @property
    def has_qa_questions(self):
        questions = Question.objects.filter(is_qa=True, section=self)
        if questions.count() > 0:
            return True
        else:
            return False
    
    @property
    def has_questions(self):
        questions = Question.objects.filter(section=self)
        if questions.count() > 0:
            return True
        else:
            return False

    @property
    def questions_count(self):
        if self.has_questions:
            questions = Question.objects.filter(section=self)
            return questions.count()
        else:
            return 0

class Question(BaseModel):
    TYPE_TEXT = 1
    TYPE_SELECT = 2
    TYPE_CHECKBOX = 3
    TYPE_BOOLEAN = 4
    TYPE_UPLOAD = 5
    TYPE_NUMBER = 6
    TPE_DATE = 7
    TYPE_TEXTBOX = 8

    ANSWER_TYPE_CHOICES = (
        (TYPE_TEXT, _("Text")),
        (TYPE_SELECT, _("Select")),
        (TYPE_CHECKBOX, _("Checkbox")),
        (TYPE_BOOLEAN, _("Boolean")),
        (TYPE_UPLOAD, _("File Upload")),
        (TYPE_NUMBER, _("Number")),
        (TPE_DATE, _("Date")),
        (TYPE_TEXTBOX, _("Textbox")),
    )

    TYPE_IN_WORDS = {
        TYPE_TEXT: _("Text"),
        TYPE_SELECT: _("Selection"),
        TYPE_CHECKBOX: _("Checkboxes"),
        TYPE_BOOLEAN: _("True/False"),
        TYPE_UPLOAD: _("File Upload"),
        TYPE_NUMBER: _("Number"),
        TPE_DATE: _("Date"),
        TYPE_TEXTBOX: _("Textbox"),
    }

    answer_type = models.IntegerField(
        choices=ANSWER_TYPE_CHOICES, default=TYPE_TEXT, blank=False, null=False
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='risk_questions')
    description = models.TextField(max_length=1000)
    trans_description = models.TextField(max_length=500, blank=True, null=True)
    short_description = models.TextField(max_length=500, blank=True, null=True)
    trans_short_description = models.TextField(blank=True, null=True)
    is_required = models.BooleanField(
        default=False,
    )
    max_score = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0, null=True
    )
    is_scored = models.BooleanField(default=True)
    is_qa = models.BooleanField(default=False)
    is_dd = models.BooleanField(default=False)
    description_slug = models.SlugField(blank=True, null=True)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return (
            self.section.category.unique_reference + " - "
            + str(self.section.short_name) + " - " + str(self.id)
        )

    def save(self, *args, **kwargs):
        self.description_slug = slugify(self.description)
        super(Question, self).save(*args, **kwargs)

    @property
    def short_description_value(self):
        short_description = self.short_description
        if short_description is not None:
            return short_description
        return self.description

    @property
    def marking_scheme(self):
        if MarkingScheme.objects.filter(question=self).count() > 0:
            return MarkingScheme.objects.filter(question=self).first()
        return None
    
    @property
    def options(self):
        if self.marking_scheme:
            return self.marking_scheme.options.split(",")
        else:
            return []

    @property
    def options_string(self):
        return ",".join([str(x) for x in self.options])

    @property
    def scores(self):
        if self.marking_scheme:
            return self.marking_scheme.score.split(",")
        else:
            return []

    @property
    def score_string(self):
        return ",".join([str(x) for x in self.scores])

    @property
    def type_text(self):
        return self.TYPE_IN_WORDS[self.answer_type]
    
    @property
    def participants(self):
        participants = []
        for response in SupplierResponse.objects.filter(question_id=self.id).distinct(
            "supplier_id", "question_id"
        ):
            participants.append(response.supplier)
        return participants


class MarkingScheme(BaseModel):
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    options = models.TextField(default="", db_index=True)
    # options = models.TextField(blank=True, null=True, default="")
    score = models.TextField(default="", db_index=True)

    class Meta:
        verbose_name = "Marking Scheme"
        verbose_name_plural = "Marking Schemes"


class SupplierResponse(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,
        related_name="risk_supplier_response", on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to=supplier_response_files, validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    options = pgcrypto.EncryptedTextField(
        max_length=100000, db_index=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Supplier Response"
        verbose_name_plural = "Supplier Responses"


class QualityAssurance(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Quality Assurance"
        verbose_name_plural = "Quality Assurances"

    def __str__(self):
        return self.title
    
    @property
    def qa_sections(self):
        return Section.has_qa_q.filter(category=self.category).order_by("id")


class QualityAssuranceQuestion(BaseModel):
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    quality_assurance = models.ForeignKey(
        QualityAssurance, blank=False, null=False, on_delete=models.CASCADE
    )
    verification_instruction = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Quality Assurance Question"
        verbose_name_plural = "Quality Assurance Questions"


class QualityAssuranceResponse(BaseModel):
    SEVERITY_CHOICES = (("High", "High"), ("Medium", "Medium"), ("Low", "Low"))
    LIKELIHOOD_CHOICES = (("Rare", "Rare"),("Unlikely", "Unlikely"), ("Possible", "Possible"), ("Likely", "Likely"), ("Almost Certain", "Almost Certain"))
    CREATED = 1
    VERIFIED = 2

    VERIFICATION_STATUS_CHOICES = (
        (CREATED, "Created"),
        (VERIFIED, "Verified"),
    )

    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE, related_name= 'risk_quality_assuarance_response'
    )
    quality_assurance_question = models.ForeignKey(
        QualityAssuranceQuestion, on_delete=models.CASCADE
    )
    number = models.CharField(max_length=200, null=True)
    date = models.DateTimeField(null=True)
    risk_description = models.TextField(null=True, blank=True)
    impact_description = models.TextField(null=True, blank=True)
    likelihood = models.CharField(
        max_length=200, choices=LIKELIHOOD_CHOICES, default="likelihood", null=True
    )
    comment = models.TextField(null=True, blank=True)
    severity = models.CharField(
        max_length=200, choices=SEVERITY_CHOICES, default="severity", null=True
    )
    document = models.FileField(
        upload_to="Rfq/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=1000,
    )
    created_by = models.ForeignKey(
        User, blank=False, related_name="risk_response_created_by",
        null=True, on_delete=models.CASCADE,
    )
    buyer = models.ForeignKey(
        'buyer.Buyer', blank=False, related_name="risk_buyer",
        null=False, on_delete=models.CASCADE
    )
    verified_by = models.ForeignKey(
        User, blank=True, related_name="risk_response_verified_by",
        null=True, on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = "Quality Assurance Response"
        verbose_name_plural = "Quality Assurance Responses"

    def __str__(self):
        return (
            self.supplier.company_name + " - " + str(self.quality_assurance_question)
            + " - " + self.severity + " - " + self.created_by.username 
        )



class SupplierSectionScore(BaseModel):
    section = models.ForeignKey(
        Section, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, related_name='supplier_section_score_risk', on_delete=models.CASCADE
    )
    score = models.BigIntegerField(db_index=True)


class SupplierCategoryScore(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, related_name='supplier_category_score_risk',on_delete=models.CASCADE
    )
    score = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, default=0
    )
    score_after_qa = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, null=True, blank=True
    )
    # weighted score
    risk_score = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, default=0
    )
    rank = models.BigIntegerField(db_index=True, default=0)
    rank_after_qa = models.BigIntegerField(db_index=True, null=True, blank=True)


class RiskReport(BaseModel):
    risk = models.ForeignKey(RiskManagement, on_delete=models.CASCADE)
    bidder_information = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation_summary = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation_responses = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_pdf = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_excel = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa = models.FileField(
        upload_to="riskmanagement/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )

    class Meta:
        verbose_name = "Risk Report"
        verbose_name_plural = "Risk Reports"

class JobSupportingDocuments(BaseModel):
    
    riskmanagement = models.ForeignKey(RiskManagement, related_name='supporting_docs', on_delete=models.CASCADE)
    
    # document = models.FileField(
    #     upload_to="riskmanagement/job/supportingdocuments/%Y/%m/%d", validators=validators,
    #     storage=PrivateMediaStorage(), blank=True, null=True,
    # )
    
    document = models.FileField(
        upload_to="riskmanagement/job/supportingdocuments/%Y/%m/%d", validators=validators,
        blank=True, null=True,
    )

    class Meta:
        ordering = ['riskmanagement']
        verbose_name = "Risk Job Supporting Document"
        verbose_name_plural = "Risk Job Supporting Documents"

    @property
    def documentname(self):
        return os.path.basename(self.document.name)
    
    @property
    def documentextension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension

class CategorySupportingDocuments(BaseModel):
    
    category = models.ForeignKey(Category, related_name='category_supporting_docs', on_delete=models.CASCADE)
    
    # document = models.FileField(
    #     upload_to="riskmanagement/category/supportingdocuments/%Y/%m/%d", validators=validators,
    #     storage=PrivateMediaStorage(), blank=True, null=True,
    # )
    
    document = models.FileField(
        upload_to="riskmanagement/category/supportingdocuments/%Y/%m/%d", validators=validators,
        blank=True, null=True,
    )

    class Meta:
        ordering = ['category']
        verbose_name = "Risk Category Supporting Document"
        verbose_name_plural = "Risk Category Supporting Documents"

    @property
    def documentname(self):
        return os.path.basename(self.document.name)
    
    @property
    def documentextension(self):
        name, extension = os.path.splitext(self.document.name)
        return extension