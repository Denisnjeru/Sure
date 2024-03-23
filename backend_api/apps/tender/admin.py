from django.contrib import admin

from apps.tender.models import *


@admin.register(Tender)
class TenderAdmin(admin.ModelAdmin):
    list_display = ["title", "unique_reference", "approved_by", "created_by"]


@admin.register(Category)
class TenderCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "unique_reference", "bid_charge", "pass_score", "is_open", "closing_date"]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_section', 'category']
    search_fields = ('name',)


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


@admin.register(Item)
class TenderItemAdmin(admin.ModelAdmin):
    list_display = [
         "description", "number", "quantity", "current_price", "outlier_score_final",
        "upper_outlier_score_final", "median_price_final", "code"
    ]

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


@admin.register(SupplierSectionScore)
class SupplierSectionScoreAdmin(admin.ModelAdmin):
    list_display = [
        'section', 'supplier', 'score', 'score_after_qa'
    ]
    search_fields = ('section_id__category_id__unique_reference', 'supplier_id__company_name')
    autocomplete_fields = ('section', 'supplier')


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ["document_type", "authoriser_name", "authoriser_role"]


@admin.register(SupplierFinancialResponse)
class SupplierFinancialResponseAdmin(admin.ModelAdmin):
    list_display = ["supplier", "category"]


admin.site.register(CategoryReport)
admin.site.register(FinancialRatio)
admin.site.register(ItemResponse)
admin.site.register(QualityAssuranceResponse)
admin.site.register(DueDiligence)
admin.site.register(SupplierCategoryScore)
admin.site.register(SupplierPDFResponse)
admin.site.register(AwardLetter)
admin.site.register(RegretLetter)
admin.site.register(SupplierTechnicalScore)
admin.site.register(SupplierFinancialTotal)
admin.site.register(Invitee)
