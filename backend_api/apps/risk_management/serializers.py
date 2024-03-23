from asyncore import read
from dataclasses import field
from datetime import datetime
from sre_constants import CATEGORY
import traceback
from unicodedata import category
from unittest.mock import seal
import pytz
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework.utils import model_meta
from rest_framework import serializers

from  apps.suppliers.models import  Supplier
from .models import (
    RiskManagement, Category, Section, Question, MarkingScheme, SupplierResponse, QualityAssurance,
    QualityAssuranceQuestion, QualityAssuranceResponse, JobSupportingDocuments, CategorySupportingDocuments
)


class RiskListSerializer(serializers.ModelSerializer):
    approved_by = serializers.SerializerMethodField("get_approved_by")
    created_by = serializers.SerializerMethodField("get_created_by")
    class Meta:
        model = RiskManagement
        fields = ['id', 'company', 'title', 'unique_reference', 'approved_by', 'created_by', 'status', 'approved']

    def get_approved_by(self, obj):
        if obj.approved_by:
            return f'{obj.approved_by.username}'
        else:
            return ''

    def get_created_by(self, obj):
        if obj.created_by:
            return f'{obj.created_by.username}'
        else:
            return ''

class RiskJobSupportingDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSupportingDocuments
        fields = ['id', 'riskmanagement', 'documentname', 'documentextension' , 'document']

class RiskCategorySupportingDocumentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySupportingDocuments
        fields = ['id', 'category', 'documentname', 'documentextension' , 'document']

class RiskApproveSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskManagement
        fields = ['approved_by', ]


class RiskQuestionRetrieveSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section_name')
    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'short_description', 'trans_short_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'description_slug'
        ]
    
    def get_section_name(self, obj):
        if obj:
            return f'{obj.section.name}'
        else:
            return ''

class RiskQuestionListSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField('get_section_name')
    verification_instruction = serializers.SerializerMethodField('get_verification_instruction')
    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'short_description', 'trans_short_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'description_slug', 'verification_instruction'
        ]
    
    def get_section_name(self, obj):
        if obj:
            return f'{obj.section.name}'
        else:
            return ''
    
    def get_verification_instruction(self, obj):
        if obj:
            qs = QualityAssuranceQuestion.objects.filter(question=obj.id).first()
            if qs:
                return f'{qs.verification_instruction}'

class RiskQuestionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question

        fields = [
            'id', 'description', 'short_description', 'trans_description','trans_short_description' ,'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_dd', 'is_qa'
        ]
        read_only = ('id', )


class RiskSectionCategoryListSerializer(serializers.ModelSerializer): 
    category = serializers.SerializerMethodField('get_category_name')
    class Meta:
        model = Section
        fields = [
            'id', 'name', 'questions_count', 'category'
        ]

    def get_category_name(self, obj):
        if obj.category:
            return f'{obj.category.name}'
        else:
            return ''

class RiskQASectionSerializer(serializers.ModelSerializer):
    risk_questions = serializers.SerializerMethodField('get_risk_questions')

    class Meta:
        model = Section
        fields = [
            'id', 'category', 'name', 'short_name', 'description', 'risk_questions'
        ]

    def get_risk_questions(self, obj):
        qs = Question.objects.filter(is_qa=True, section=obj)
        ser = RiskQuestionListSerializer(instance=qs, many=True)
        return ser.data 

class RiskSectionListSerializer(serializers.ModelSerializer):
    parent_section = serializers.SerializerMethodField('get_parent_section_name')
    category = serializers.SerializerMethodField('get_category_name')

    class Meta:
        model = Section
        fields = [
            'id', 'name', 'short_name', 'description','parent_section', 'category'
        ]
    
    def get_category_name(self, obj):
        if obj:
            return f'{obj.category.name}'
        else:
            return ''
    
    def get_parent_section_name(self, obj):
        if obj:
            return f'{obj.category.ame}'
        else:
            return ''

class RiskSectionRetrieveSerializer(serializers.ModelSerializer):
    parent_section = serializers.SerializerMethodField('get_parent_section_name')
    category = serializers.SerializerMethodField('get_category_name')
    risk_questions = RiskQuestionListSerializer(many=True)
    class Meta:
        model = Section
        fields = [
            'id', 'name', 'short_name', 'trans_name','description', 'parent_section', 'category',
            'risk_questions'
        ]
    
    def get_category_name(self, obj):
        if obj:
            return f'{obj.category.name}'
        else:
            return ''
    
    def get_parent_section_name(self, obj):
        if obj:
            return f'{obj.category.name}'
        else:
            return ''


class RiskSectionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'id', 'name', 'short_name', 'description', 'parent_section', 'category', 'trans_name',
        ]
        read_only = ('id', )

class RiskCategoryListSerializer(serializers.ModelSerializer):
    category_type = serializers.SerializerMethodField("get_category_type")
    currency = serializers.SerializerMethodField("get_currency")

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'opening_date', 'category_type', 'currency',
            'closing_date', 'is_open'
        ]
    
    def get_category_type(self, obj):
        if obj.category_type:
            return f'{obj.category_type.name}'
        else:
            return ''

    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''

class SupplierParticipantsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Supplier
        fields = [
            'id','company_name', 'short_name', 'contact_name','kra_pin_number'
        ]

class RiskCategoryRetrieveSerializer(serializers.ModelSerializer):
    category_type = serializers.SerializerMethodField("get_category_type")
    currency = serializers.SerializerMethodField("get_currency")
    risk_sections = RiskSectionCategoryListSerializer(many=True)
    category_supporting_docs = RiskCategorySupportingDocumentsSerializer(many=True)
    participants = serializers.SerializerMethodField("get_participants")
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'opening_date', 'category_type', 'currency',
            'closing_date', 'is_open', 'participants', 'risk_sections' ,'category_supporting_docs', 'has_risk_assessment'
        ]

    def get_category_type(self, obj):
        if obj.category_type:
            return f'{obj.category_type.name}'
        else:
            return ''

    def get_currency(self, obj):
        if obj.currency:
            return f'{obj.currency.initials}'
        else:
            return ''
    
    def get_participants(self, obj):
        participants = obj.participants
        return SupplierParticipantsSerializer(participants, many=True).data


class RiskRetrieveSerializer(serializers.ModelSerializer):
    approved_by = serializers.SerializerMethodField("get_approved_by")
    created_by = serializers.SerializerMethodField("get_created_by")
    supporting_docs = RiskJobSupportingDocumentsSerializer(many=True)
    risk_categories = RiskCategoryListSerializer(many=True)

    class Meta:
        model = RiskManagement
        fields = ['id', 'company', 'title', 'unique_reference', 'approved_by', 'created_by', 'status', 'approved', 'questions_template', 'supporting_docs', 'risk_categories']

    def get_approved_by(self, obj):
        if obj.approved_by:
            return f'{obj.approved_by.username}'
        else:
            return ''

    def get_created_by(self, obj):
        if obj.created_by:
            return f'{obj.created_by.username}'
        else:
            return ''

class RiskCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskManagement
        fields = [
            'id', 'title', 'unique_reference', 'send_participant_list_to_supplier', 'created_by', 'company'
        ]
        read_only= ('id', )


def validate_date(opening_date, closing_date):
    # Validating the opening and closing dates 
    utc = pytz.UTC
    open_date = opening_date
    close_date = closing_date
    time_now = utc.localize(datetime.now())
        
    if time_now > close_date or close_date < open_date:
        raise ValidationError(
            _("The opening date, closing date and today's date dont compare well."),
        )
    elif close_date > open_date < time_now:
        return True
    elif close_date > open_date > time_now:
        return False

class RiskCategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'pass_score',
            'opening_date', 'closing_date', 'evaluation_date', 'currency', 'is_open',
            'invite_only', 'allowed_staff', 'send_participant_list_to_supplier', 'riskmanagement', 'parent_category',
            'category_type'
        ]
        read_only = ('id', )

    def create(self, validated_data):
        """
        We have a bit of extra checking around this in order to provide
        descriptive messages when something goes wrong, but this method is
        essentially just:
            return ExampleModel.objects.create(**validated_data)
        If there are many to many fields present on the instance then they
        cannot be set until the model is instantiated, in which case the
        implementation is like so:
            example_relationship = validated_data.pop('example_relationship')
            instance = ExampleModel.objects.create(**validated_data)
            instance.example_relationship = example_relationship
            return instance
        The default implementation also does not handle nested relationships.
        If you want to support writable nested relationships you'll need
        to write an explicit `.create()` method.
        """

        ModelClass = self.Meta.model

        # Remove many-to-many relationships from validated_data.
        # They are not valid arguments to the default `.create()` method,
        # as they require that the instance has already been saved.
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            validated_data['is_open'] = validate_date(validated_data['opening_date'], validated_data['closing_date'])
            instance = ModelClass._default_manager.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.%s.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.%s.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    ModelClass.__name__,
                    ModelClass._default_manager.name,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        # Save many-to-many relationships after the instance is created.
        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

class RiskMarkingSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingScheme
        fields = [
            'id', 'question', 'options', 'score'
        ]


class RiskSRSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierResponse
        fields = [
            'id', 'question', 'supplier', 'document_url', 'options'
        ]


class RiskQASerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssurance
        fields = [
            'id', 'category', 'title'
        ]
        read_only = ('id',)

class RiskQAInstructionSerializer(serializers.ModelSerializer):
    qa_sections = serializers.SerializerMethodField('get_qa_sections')
    category = serializers.SerializerMethodField('get_category')
    class Meta:
        model = QualityAssurance
        fields = [
            'id', 'category', 'title', 'qa_sections'
        ]

        read_only = ('id',)

    def get_qa_sections(self, obj):
        qasecs = obj.qa_sections
        ser = RiskQASectionSerializer(instance=qasecs, many=True)
        return ser.data
    
    def get_category(self, obj):
        if obj.category:
            return f'{obj.category.name}'
        else:
            return ''


class RiskQAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssuranceQuestion
        fields = [
            'id', 'question', 'quality_assurance', 'verification_instruction'
        ]
        read_only = (
            'id'
        )



class RiskQARSerializer(serializers.ModelSerializer):
    supplier = serializers.SerializerMethodField("get_supplier_company_name")
    quality_assurance_question = serializers.SerializerMethodField("get_quality_assurance_question")
    class Meta:
        model = QualityAssuranceResponse
        fields = [
            'id', 'supplier','risk_description', 'impact_description','quality_assurance_question', 'number', 'date',
            'comment', 'severity', 'likelihood','document', 'created_by', 'verified_by', 'buyer'
        ]

    def get_supplier_company_name(self, obj):
        if obj.supplier:
            return f'{obj.supplier.company_name}'
        else:
            return ''

    def get_quality_assurance_question(self, obj):
        if obj.quality_assurance_question:
            return f'{obj.quality_assurance_question.question.description}'
        else:
            return ''