from django.contrib import admin
from .models import (
    Prequalification, Category, Section, SupplierResponse, Question, MarkingScheme, QualityAssurance,
    QualityAssuranceQuestion, QualityAssuranceResponse, DueDiligence, SupplierCategoryScore, AwardLetter,
    SupplierSectionScore, SupplierPDFResponse, JobReport, FinancialRatio, CategoryReport, ClientDocument,
    CategoryInvite, RegretLetter, CustomLetter, DueDilligenceLetter, QaTccResponse, QaCr12Response,
    QaBusinessPermitResponse, QaPinCertificateResponse, QaNcaaResponse, QaPoisonsBoardResponse,
    QaIncorporationCertificateResponse
)

# Register your models here.
@admin.register(Prequalification)
class PrequalificationAdmin(admin.ModelAdmin):
    list_display = [
        "company",
        "title",
        "unique_reference",
    ]
    list_filter = [
        "company__company_name",
        "title",
        "unique_reference",
    ]
    search_fields = [
        "company__company_name",
        "title",
        "unique_reference",
    ]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "unique_reference",
        "bid_charge",
        "opening_date",
        "closing_date",
        "category_type"
    ]

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_section', 'category']


@admin.register(SupplierResponse)
class SupplierResponseAdmin(admin.ModelAdmin):
    list_display = ['question', 'supplier', 'options']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['description', 'short_description', 'max_score', 'is_scored', 'is_qa', 'is_dd']
    search_fields = ('description', 'id')


@admin.register(MarkingScheme)
class MarkingSchemeAdmin(admin.ModelAdmin):
    list_display = ['options', 'score', 'question']


@admin.register(QualityAssurance)
class QualityAssuranceAdmin(admin.ModelAdmin):
    list_display = ['title', 'category']


@admin.register(QualityAssuranceQuestion)
class QualityAssuranceQuestionAdmin(admin.ModelAdmin):
    list_display = ['question', 'verification_instruction']
    search_fields = ('question_id__description',)
    autocomplete_fields = ('question', )


@admin.register(AwardLetter)
class AwardLettersAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "category",
        "award_date",
        "get_job_name",
        "get_company_name",
    )
    search_fields = (
        "supplier",
        "category",
        "award_date",
        "category_id__prequalification_id__job_title",
        "category_id__company_id__company_name",
    )

    def get_job_name(self, obj):
        return obj.category.prequalification.title

    get_job_name.short_description = "Job Title"

    def get_company_name(self, obj):
        return obj.category.prequalification.company.company_name

    get_company_name.short_description = "Company Name"


@admin.register(RegretLetter)
class RegretLettersAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "category",
        "regret_date",
        "get_job_name",
        "get_company_name",
    )
    search_fields = (
        "supplier",
        "category",
        "regret_date",
        "category_id__prequalification_id__job_title",
        "category_id__company_id__company_name",
    )

    def get_job_name(self, obj):
        return obj.category.prequalification.title

    get_job_name.short_description = "Job Title"

    def get_company_name(self, obj):
        return obj.category.prequalification.company.company_name

    get_company_name.short_description = "Company Name"


@admin.register(CustomLetter)
class CustomLettersAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "category",
        "custom_letter_date",
        "get_job_name",
        "get_company_name",
    )
    search_fields = (
        "supplier",
        "category",
        "custom_letter_date",
        "category_id__prequalification_id__job_title",
        "category_id__company_id__company_name",
    )

    def get_job_name(self, obj):
        return obj.category.prequalification.title

    get_job_name.short_description = "Job Title"

    def get_company_name(self, obj):
        return obj.category.prequalification.company.company_name

    get_company_name.short_description = "Company Name"


@admin.register(DueDilligenceLetter)
class DDLettersAdmin(admin.ModelAdmin):
    list_display = (
        "supplier",
        "category",
        "due_dilligence_letter_date",
        "get_job_name",
        "get_company_name",
    )
    search_fields = (
        "supplier",
        "category",
        "due_dilligence_letter_date",
        "category_id__prequalification_id__job_title",
        "category_id__company_id__company_name",
    )

    def get_job_name(self, obj):
        return obj.category.prequalification.title

    get_job_name.short_description = "Job Title"

    def get_company_name(self, obj):
        return obj.category.prequalification.company.company_name

    get_company_name.short_description = "Company Name"


@admin.register(QaTccResponse)
class QaTccResponseAdmin(admin.ModelAdmin):
    list_display = [
        'qa_response', 'pin_number', 'pin_number_outcome', 'company_name', 'expiry_date',
        'expiry_date_outcome'
    ]


@admin.register(QaCr12Response)
class QaCr12ResponseAdmin(admin.ModelAdmin):
    list_display = [
        'qa_response', 'company_number', 'company_number_outcome', 'document_date'
    ]


@admin.register(QaBusinessPermitResponse)
class QaBusinessPermitResponseAdmin(admin.ModelAdmin):
    list_display = [
        'qa_response', 'business_name', 'business_name_outcome', 'business_id', 'date'
    ]


@admin.register(QaPinCertificateResponse)
class QaPinCertificateResponseAdmin(admin.ModelAdmin):
    list_display = [
        'qa_response', 'pin_number', 'tax_pin_outcome'
    ]


@admin.register(QaNcaaResponse)
class QaNcaaResponseAdmin(admin.ModelAdmin):
    list_display = [
        'qa_response', 'serial_number', 'expiry_date'
    ]


@admin.register(QaPoisonsBoardResponse)
class QaPoisonsBoardResponseAdmin(admin.ModelAdmin):
    list_display = [
        "qa_response", "company_name", "company_name_outcome",
        "expiry_date", "expiry_date_outcome"
    ]


@admin.register(QaIncorporationCertificateResponse)
class QaIncorporationCertificateResponseAdmin(admin.ModelAdmin):
    list_display = [
        "qa_response", "company_name", "company_name_outcome",
        "company_number", "company_number_outcome"
    ]


# @admin.register(SupplierResponse)
# class SupplierResponseAdmin(admin.ModelAdmin):
#     list_display = ['question_id__description', 'supplier']


admin.site.register(ClientDocument)
admin.site.register(CategoryReport)
admin.site.register(FinancialRatio)
admin.site.register(QualityAssuranceResponse)
admin.site.register(DueDiligence)
admin.site.register(SupplierCategoryScore)
admin.site.register(SupplierSectionScore)
admin.site.register(SupplierPDFResponse)
admin.site.register(JobReport)
admin.site.register(CategoryInvite)