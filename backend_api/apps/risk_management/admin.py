from pyexpat import model
from re import search
from django.contrib import admin
from django.template.loader import render_to_string
from .models import (
    RiskManagement, Category, Section, Question, MarkingScheme, SupplierCategoryScore, SupplierResponse, QualityAssurance,
    QualityAssuranceQuestion, QualityAssuranceResponse, JobSupportingDocuments, CategorySupportingDocuments
)

class RiskCategoryInline(admin.TabularInline):
    model = Category
    fk_name = "riskmanagement"
    extra = 1
@admin.register(RiskManagement)
class RiskManagementAdmin(admin.ModelAdmin):
    ordering = ["company","unique_reference"]
    search_fields = ('company', 'title', 'unique_reference')

    list_display = (
        "title",
        "unique_reference",
        "lang_en"
    )

    inlines = [RiskCategoryInline, ]

@admin.register(Category)
class RiskCategory(admin.ModelAdmin):
    ordering = ['riskmanagement', 'opening_date']
    search_fields = ('name', 'trans_name', 'category_type')

    list_display = (
        "name",
        "trans_name",
        "unique_reference",
        "bid_charge",
        "opening_date",
        "closing_date",
        "evaluation_date",
        "category_type"
    )

    list_filter = [
        "opening_date",
        "closing_date",
        "is_open",
        "category_type"
    ]

@admin.register(Section)
class RiskSection(admin.ModelAdmin):
    ordering = ('name', 'trans_name', 'short_name', 'description', 
    'parent_section', 'category', 'name_slug')
    search_fields = ('name', 'trans_name', 'short_name', 'description', 
    'parent_section', 'category', 'name_slug')

    list_display = (
        'name', 
        'trans_name', 
        'short_name', 
        'description', 
        'parent_section', 
        'category', 
        'name_slug'
    )

    list_filter = [
        "category",
    ]

@admin.register(Question)
class RiskQuestion(admin.ModelAdmin):
    ordering = ('description', 'trans_description', 'short_description',
    'trans_short_description', 'section', 'answer_type', 'is_required', 'is_qa', 'is_dd')
    search_fields = ('description', 'trans_description', 'short_description',
    'trans_short_description', 'section', 'answer_type', 'is_required', 'is_qa', 'is_dd') 

    list_display = (
        'description', 
        'trans_description', 
        'short_description',
        'trans_short_description',
        'section', 
        'answer_type', 
        'is_required', 
        'is_qa', 
        'is_dd'
    )

    list_filter = [
        "answer_type",
        "section",
        "is_qa",
        "is_required"
    ]

@admin.register(MarkingScheme)
class RiskMarkingScheme(admin.ModelAdmin):
    ordering = ('question', 'options', 'score')
    search_fieldS = ('question', 'options', 'score')

    list_display = (
        'question',
        'options',
        'score'
    )
        
    list_filter = [
        "question",
    ]


@admin.register(SupplierResponse)
class RiskSupplierResponse(admin.ModelAdmin):
    ordering = ['question', 'supplier']
    search_fields = ('question', 'supplier',)

    list_display = (
        "question",
        "supplier",
    )

    list_filter = [
        "question",
        "supplier",
    ]


@admin.register(QualityAssurance)
class RiskQualityAssurance(admin.ModelAdmin):
    ordering = ('category', 'title')
    search_fields = ('category', 'title')

    list_display = (
        'category',
        'title'
    )

    list_filter = [
        "category",
    ]

@admin.register(QualityAssuranceQuestion)
class RiskQualityAssuranceQuestion(admin.ModelAdmin):
    ordering = ('question', 'quality_assurance', 'verification_instruction')
    search_fields = ('question', 'quality_assurance', 'verification_instruction')

    list_display = (
        'question', 
        'quality_assurance', 
        'verification_instruction'
    )

    list_filter = [
        "question",
        "quality_assurance"
    ]


@admin.register(QualityAssuranceResponse)
class RiskQualityAssuranceResponse(admin.ModelAdmin):
    ordering = ('supplier', 'quality_assurance_question', 'date', 'likelihood', 'severity', 'created_by', 'buyer', 'verified_by')
    search_fields = ('supplier', 'quality_assurance_question', 'date', 'likelihood', 'severity', 'created_by', 'buyer', 'verified_by')

    list_display = (
        'supplier', 
        'quality_assurance_question', 
        'date', 
        'likelihood', 
        'severity', 
        'created_by', 
        'buyer', 
        'verified_by'
    )

    list_filter = [
        "supplier",
        "quality_assurance_question",
        "created_by",
        "buyer",
        "created_by",
        "verified_by"
    ]
@admin.register(SupplierCategoryScore)
class RiskSupplierCategoryScore(admin.ModelAdmin):
    ordering = ('category', 'supplier', 'score', 'score_after_qa', 'risk_score', 'rank', 'rank_after_qa')
    search_fields = ('category', 'supplier', 'score', 'score_after_qa', 'risk_score', 'rank', 'rank_after_qa')

    list_display = (
        'category', 
        'supplier', 
        'score', 
        'score_after_qa', 
        'risk_score', 
        'rank', 
        'rank_after_qa'
    )

@admin.register(JobSupportingDocuments)
class RiskSupportingDocuments(admin.ModelAdmin):
    ordering = ["riskmanagement", ]
    search_fields = ('riskmanagement', )

    list_display = (
        "riskmanagement",
        "documentname",
        "documentextension"
    )

    list_filter = [
        "riskmanagement",
    ]
@admin.register(CategorySupportingDocuments)
class RiskSupportingDocuments(admin.ModelAdmin):
    ordering = ["category", ]
    search_fields = ('category', )

    list_display = (
        "category",
        "documentname",
        "documentextension"
    )

    list_filter = [
        "category",

    ]
