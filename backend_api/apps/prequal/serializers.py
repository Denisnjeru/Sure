import datetime
import traceback

from django import apps
from django.utils import timezone
from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta
from sentry_sdk import capture_exception

from apps.prequal.models import (
    FinancialRatio, Prequalification, Category, Section, Question, DueDiligence, MarkingScheme, SupplierResponse, QualityAssurance,
    QualityAssuranceQuestion, QualityAssuranceResponse, DueDiligenceSupplier, DueDiligenceQuestion,
    SupplierCategoryScore, AwardLetter, RegretLetter, CategoryInvite, ClientDocument, CustomLetter, DueDilligenceLetter,
    QaTccResponse, QaIncorporationCertificateResponse, QaCr12Response, QaBusinessPermitResponse, QaNcaaResponse,
    QaPoisonsBoardResponse, QaNationalIdResponse, QaPinCertificateResponse
)
from apps.prequal.tasks import ConductOcr, existing_supplier_email_invite, non_existent_invites_email
from .utils import calculate_financial_ratios_after_qa


class JobListSerializer(serializers.ModelSerializer):
    approved_by = serializers.SerializerMethodField()
    is_open = serializers.SerializerMethodField()
    has_participants = serializers.SerializerMethodField()

    class Meta:
        model = Prequalification
        fields = [
            'id', 'title', 'unique_reference', 'status', 'approved_by', 'is_open',
            'show_bids', 'advert', 'current_suppliers', 'has_participants'
        ]

    def get_approved_by(self, obj):
        if obj.approved_by:
            return f"{obj.approved_by.first_name} {obj.approved_by.last_name}"
        else:
            return ""

    def get_is_open(self, obj):
        if Category.objects.filter(is_open=True, prequalification_id=obj.id).count() > 0:
            return True
        else:
            return False

    def get_has_participants(self, obj):
        s = SupplierResponse.objects.filter(question__section__category__prequalification_id=obj.id)
        if s.count() > 0:
            return True
        else:
            return False


class JobCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prequalification
        fields = [
            'id', 'title', 'unique_reference', 'show_bids', 'advert', 'current_suppliers', 'bidding_instructions',
            'company', 'criteria_country'
        ]

class JobUpdateCurrentSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prequalification
        fields = ['current_suppliers',]

class JobCatSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prequalification
        fields = [
            'category_suppliers',
        ]

class JobUpdateCurrentSupplierLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prequalification
        fields = ['current_suppliers_letter',]

class JobExcelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prequalification
        fields = ['question_template']


class CriteriaCountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.apps.get_model('core', 'CriteriaCountry')
        fields = ['id', 'name']
        ref_name = 'PCriteriaCountrySerializer'


class CategoryListSerializer(serializers.ModelSerializer):
    has_participants = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    has_qa_instance = serializers.SerializerMethodField()
    has_dd_instance = serializers.SerializerMethodField()
    job_name = serializers.SerializerMethodField()
    job_type = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'currency', 'question_template', 'opening_date',
            'closing_date', 'is_open', 'has_participants', 'participants', 'category_type', 'has_qa_instance', 'has_dd_instance',
            'invite_only', 'send_participant_list_to_supplier', 'job_name','job_type'
        ]

    def get_has_participants(self, obj):
        s = SupplierResponse.objects.filter(question__section__category_id=obj.id)
        if s.count() > 0:
            return True
        else:
            return False

    def get_job_name(self, obj):
        return obj.prequalification.title

    def get_job_type(self, obj):
        return 'Prequal'

    def get_participants(self, obj):
        s = SupplierResponse.objects.filter(question__section__category_id=obj.id).count()
        return s

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%dT%H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%dT%H:%M")

    def get_has_qa_instance(self, obj):
        if QualityAssurance.objects.filter(category_id=obj.id).first() is not None:
            return True
        else:
            return False

    def get_has_dd_instance(self, obj):
        if DueDiligence.objects.filter(category_id=obj.id).first() is not None:
            return True
        else:
            return False


class LetterJobListSerializer(serializers.ModelSerializer):
    is_open = serializers.SerializerMethodField()
    has_custom_letter = serializers.SerializerMethodField()
    has_regret_letter = serializers.SerializerMethodField()
    has_success_letter = serializers.SerializerMethodField()
    has_dd_letter = serializers.SerializerMethodField()

    class Meta:
        model = Prequalification
        fields = [
            'id', 'title', 'unique_reference', 'status', 'approved_by', 'is_open',
            'has_custom_letter', 'has_regret_letter', 'has_success_letter', 'has_dd_letter'
        ]

    def get_is_open(self, obj):
        if Category.objects.filter(is_open=True, prequalification_id=obj.id).count() > 0:
            return True
        else:
            return False

    def get_has_custom_letter(self, obj):
        custom_letter = ClientDocument.objects.filter(
            document_type=ClientDocument.CUSTOM, prequalification_id=obj.id)
        if custom_letter.exists():
            return True
        return False

    def get_has_regret_letter(self, obj):
        regret_letter = ClientDocument.objects.filter(
            document_type=ClientDocument.REGRET, prequalification_id=obj.id
        )
        if regret_letter.exists():
            return True
        return False

    def get_has_success_letter(self, obj):
        success_letter = ClientDocument.objects.filter(
            document_type=ClientDocument.SUCCESS, prequalification_id=obj.id
        )
        if success_letter.exists():
            return True
        return False

    def get_has_dd_letter(self, obj):
        dd_letter = ClientDocument.objects.filter(
            document_type=ClientDocument.DD, prequalification_id=obj.id
        )
        if dd_letter.exists():
            return True
        return False


class CategoryRetrieveSerializer(serializers.ModelSerializer):
    # is_open = serializers.SerializerMethodField()
    has_participants = serializers.SerializerMethodField()
    opening_date = serializers.SerializerMethodField()
    closing_date = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    has_qa_instance = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'opening_date',
            'closing_date', 'is_open', 'prequalification', 'is_open', 'pass_score', 'participants',
            'has_participants', 'currency', 'category_type', 'has_qa_instance',
            'invite_only', 'send_participant_list_to_supplier'
        ]
        depth = 2

    # def get_is_open(self, obj):
    #     if Category.objects.filter(is_open=True, obj.).count() > 0:
    #         return True
    #     else:
    #         return False

    def get_opening_date(self, obj):
        return obj.opening_date.strftime("%Y-%m-%dT%H:%M")

    def get_closing_date(self, obj):
        return obj.closing_date.strftime("%Y-%m-%dT%H:%M")

    def get_participants(self, obj):
        suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=obj.id).only('supplier_id').values('supplier_id').distinct()
        )
        return SupplierSerializer(suppliers, many=True).data

    # def get_sections(self, obj):
    #     sections = Section.objects.filter(category_id=obj.id)
    #     return SectionListSerializer(sections, many=True).data

    def get_has_participants(self, obj):
        s = SupplierResponse.objects.filter(question__section__category_id=obj.id)
        if s.count() > 0:
            return True
        else:
            return False

    def get_has_qa_instance(self, obj):
        if QualityAssurance.objects.filter(category_id=obj.id).first() is not None:
            return True
        else:
            return False


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'pass_score',
            'opening_date', 'closing_date', 'currency',
            'invite_only', 'send_participant_list_to_supplier','prequalification',
            'category_type', 'question_template'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            unq = f'{instance.prequalification.unique_reference}_{validated_data["unique_reference"]}'
            instance.unique_reference = unq
            instance.save()
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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        unq = f'{instance.prequalification.unique_reference}_{validated_data["unique_reference"]}'
        instance.unique_reference = unq
        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class CategoryDuplicateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'trans_name', 'unique_reference', 'bid_charge', 'pass_score',
            'opening_date', 'closing_date', 'currency',
            'invite_only', 'send_participant_list_to_supplier', 'prequalification',
            'category_type', 'is_open'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model

        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            unq = f'{instance.prequalification.unique_reference}_{validated_data["unique_reference"]}'
            instance.unique_reference = unq
            instance.save()

            # filesprequal = request.FILES.getlist("supporting_document_url")
            # for f in filesprequal:
            #     file_instance = Supportingdocument.objects.create(
            #         name=f.name,
            #         supporting_document_url=f,
            #         prequalification=prequalification,
            #     )
            #     file_instance_new = file_instance
            #     file_instance_new.save()

            old_category = Category.objects.filter(id=self.context['category_id']).first()

            for section in old_category.sections:
                new_parent_section = None
                if section.parent_section:
                    new_parent_section, created = Section.objects.update_or_create(
                        category_id=instance.id, name=section.parent_section.name,
                        description=section.parent_section.description,
                        short_name=section.parent_section.short_name,
                    )
                new_section, created = Section.objects.update_or_create(
                    category=instance.id, name=section.name, description=section.description,
                    parent_section=new_parent_section, short_name=section.short_name,
                )

                for question in section.questions:
                    new_question, created = Question.objects.update_or_create(
                        answer_type=question.answer_type, section=new_section,
                        description=question.description, short_description=question.short_description,
                        is_required=question.is_required, max_score=question.max_score,
                        is_scored=question.is_scored, is_qa=question.is_qa, is_dd=question.is_dd,
                    )
                    if question.answer_type == Question.TYPE_CHECKBOX or question.answer_type == Question.TYPE_SELECT:
                        if question.marking_scheme is not None:
                            MarkingScheme.objects.update_or_create(
                                question_id=new_question.id, options=question.marking_scheme.options,
                                score=question.marking_scheme.score,
                            )
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


class CategoryOpenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["closing_date"]

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        now = timezone.now()
        if validated_data['closing_date'] > now:
            instance.is_open = True
            instance.save()
            for attr, value in m2m_fields:
                field = getattr(instance, attr)
                field.set(value)

            return instance


class SectionListSerializer(serializers.ModelSerializer):
    question_count = serializers.SerializerMethodField()
    prequal_id = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'id', 'name', 'trans_name', 'parent_section', 'category', 'question_count',
            'short_name', 'description', 'prequal_id'
        ]

    def get_question_count(self, obj):
        return Question.objects.filter(section_id=obj.id).count()

    def get_prequal_id(self, obj):
        return obj.category.prequalification_id


class SectionCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = [
            'id', 'name', 'trans_name', 'short_name', 'description', 'parent_section', 'category',
        ]


class QuestionListSerializer(serializers.ModelSerializer):
    answer_type = serializers.SerializerMethodField()
    options = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'options', 'score'
        ]

    def get_answer_type(self, obj):
        return obj.get_answer_type_display()

    def get_options(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.options
        else:
            return ''

    def get_score(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.score
        else:
            return ''


class QuestionRetrieveSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'options', 'score'
        ]

    def get_options(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.options
        else:
            return ''

    def get_score(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.score
        else:
            return ''


class QuestionCreateUpdateSerializer(serializers.ModelSerializer):
    options = serializers.CharField(max_length=3000, required=False, allow_blank=True)
    score = serializers.CharField(max_length=3000, required=False, allow_blank=True)

    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', "is_qa", "is_dd", "options", "score"
        ]

    def create(self, validated_data):
        options = validated_data.pop('options')
        score = validated_data.pop('score')

        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            MarkingScheme.objects.update_or_create(
                question_id=instance.id,
                defaults={
                    "score": score,
                    "options": options
                }
            )
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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)

        options = validated_data.pop('options')
        score = validated_data.pop('score')

        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        MarkingScheme.objects.update_or_create(
            question_id=instance.id,
            defaults={
                "score": score,
                "options": options
            }
        )
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class MarkingSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarkingScheme
        fields = [
            'id', 'question', 'options', 'score'
        ]


class SRSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierResponse
        fields = [
            'id', 'question', 'supplier', 'document_url', 'options'
        ]

class SRDocumentSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    document_url = serializers.SerializerMethodField()

    class Meta:
        model = SupplierResponse
        fields = [
            'id', 'question', 'name', 'document_url'
        ]

    def get_name(self, obj):
        return obj.question.short_description

    def get_document_url(self, obj):
        return obj.document_response_url


class QASerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssurance
        fields = [
            'id', 'category', 'title'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            for question in Question.objects.filter(section__category_id=validated_data['category'], is_qa=True):
                QualityAssuranceQuestion.objects.update_or_create(
                    question_id=question.id,
                    quality_assurance_id=instance.id
                )

            conduct_ocr = ConductOcr()
            conduct_ocr.delay(category_id=instance.category_id)
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


class QAQListSerializer(serializers.ModelSerializer):
    question_type = serializers.SerializerMethodField()

    class Meta:
        model = QualityAssuranceQuestion
        fields = [
            'id', 'question', 'quality_assurance', 'verification_instruction', 'question_type'
        ]
        depth = 2

    def get_question_type(self, obj):
        if obj.question.short_description.lower() == "Tax compliance".lower():
            question_type = "tcc"
        elif obj.question.short_description.lower() == "Certificate of Incorporation".lower() or \
            "Registration certificate".lower():
            question_type = "coi"
        elif obj.question.short_description.lower() == "CR12 Certificate or equivalent".lower():
            question_type = "cr12"
        elif obj.question.short_description.lower() == "Pharmacy and poisons board License".lower():
            question_type = "ppb"
        elif obj.question.short_description.lower() == "National identification number".lower():
            question_type = "id"
        elif obj.question.short_description.lower() == "PIN certificate".lower():
            question_type = "pin"
        elif obj.question.short_description.lower() == "County government business permit".lower():
            question_type = "bp"
        elif obj.question.short_description.lower() == "NCA Registration certificate".lower():
            question_type = "nca_c"
        else:
            question_type = "normal"

        return question_type


class QAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssuranceQuestion
        fields = [
            'id', 'question', 'quality_assurance', 'verification_instruction'
        ]


class QARSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityAssuranceResponse
        fields = [
            'id', 'supplier', 'quality_assurance_question', 'number', 'date',
            'comment', 'outcome', 'score_after_qa',
            'created_by', 'verified_by'
        ]


class QARRetrieveSerializer(serializers.ModelSerializer):
    date = serializers.SerializerMethodField()
    tcc = serializers.SerializerMethodField()
    incorporation = serializers.SerializerMethodField()
    cr12 = serializers.SerializerMethodField()
    business_permit = serializers.SerializerMethodField()
    nca = serializers.SerializerMethodField()
    poisons_board = serializers.SerializerMethodField()
    national_id = serializers.SerializerMethodField()
    tax_pin = serializers.SerializerMethodField()

    class Meta:
        model = QualityAssuranceResponse
        fields = [
            'id', 'supplier', 'quality_assurance_question', 'number', 'date',
            'comment', 'outcome', 'score_after_qa',
            'created_by', 'verified_by', 'tcc', 'incorporation', 'cr12', 'business_permit', 'nca', 'poisons_board',
            'national_id', 'tax_pin'
        ]

    def get_date(self, obj):
        date = obj.date
        if date:
            return date.strftime("%Y-%m-%d")
        return

    def get_tcc(self, obj):
        tcc_response = QaTccResponse.objects.filter(qa_response_id=obj.id).first()
        return QaTccResponseSerializer(tcc_response, many=False).data

    def get_incorporation(self, obj):
        response = QaIncorporationCertificateResponse.objects.filter(qa_response_id=obj.id).first()
        return QaIncorporationCertificateResponseSerializer(response, many=False).data

    def get_cr12(self, obj):
        response = QaCr12Response.objects.filter(qa_response_id=obj.id).first()
        return QaCr12ResponseSerializer(response, many=False).data

    def get_business_permit(self, obj):
        response = QaBusinessPermitResponse.objects.filter(qa_response_id=obj.id).first()
        return QaBusinessPermitResponseSerializer(response, many=False).data

    def get_nca(self, obj):
        response = QaNcaaResponse.objects.filter(qa_response_id=obj.id).first()
        return QaNcaaResponseSerializer(response, many=False).data

    def get_poisons_board(self, obj):
        response = QaPoisonsBoardResponse.objects.filter(qa_response_id=obj.id).first()
        return QaPoisonsBoardResponseSerializer(response, many=False).data

    def get_national_id(self, obj):
        response = QaNationalIdResponse.objects.filter(qa_response_id=obj.id).first()
        return QaNationalIdResponseSerializer(response, many=False).data

    def get_tax_pin(self, obj):
        response = QaPinCertificateResponse.objects.filter(qa_response_id=obj.id).first()
        return QaPinCertificateResponseSerializer(response, many=False).data


class QaTccResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaTccResponse
        fields = ["id", "pin_number", "pin_number_outcome", "company_name", "expiry_date", "expiry_date_outcome"]


class QaIncorporationCertificateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaIncorporationCertificateResponse
        fields = ["id", "company_number", "company_name", "company_number_outcome", "company_name_outcome"]


class QaCr12ResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaCr12Response
        fields = [
            "id", "qa_response", "company_number", "company_number_outcome",
            "directors", "document_date", "directors_outcome"
        ]


class QaBusinessPermitResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaBusinessPermitResponse
        fields = ["id", "business_name", "business_id", "date", "qa_response", "business_name_outcome"]


class QaNcaaResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaNcaaResponse
        fields = ["id", "serial_number", "expiry_date", "qa_response", "expiry_date_outcome"]


class QaPoisonsBoardResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaPoisonsBoardResponse
        fields = [
            "id", "company_name", "expiry_date", "qa_response", "expiry_date_outcome",
            "company_name_outcome"
        ]


class QaNationalIdResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = QaNationalIdResponse
        fields = ["id", "name", "id_number", "qa_response"]


class QaPinCertificateResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model= QaPinCertificateResponse
        fields = ["id", "pin_number", "qa_response", "tax_pin_outcome"]


class DueDiligenceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDiligence
        fields = [
            'id', 'category', 'created_by'
        ]


class DueDiligenceSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDiligenceSupplier
        fields = ['id', 'supplier']
        depth = 2


class DueDiligenceQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDiligenceQuestion
        fields = ['id', 'question', 'due_diligence_response']
        depth = 2


class DueDiligenceQuestionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDiligenceQuestion
        fields = ['question', 'due_diligence_response', 'due_diligence_supplier']


class DueDiligenceCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDiligence
        fields = ['id', 'category', 'created_by']

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(
                **validated_data, created_by_id=self.context['request'].user.id
            )

            suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
                id__in=SupplierResponse.objects.filter(
                    question__section__category_id=instance.category_id).only('supplier_id').values('supplier_id')
            )
            # consider bidders who paid but did not participate

            dd_supplier_ids = []
            for supplier in suppliers:
                dd_supplier, created = DueDiligenceSupplier.objects.update_or_create(
                    supplier_id=supplier.id,
                    due_diligence_id=instance.id
                )
                dd_supplier_ids.append(dd_supplier.id)

            questions = Question.objects.filter(section__category_id=validated_data['category'], is_dd=True)
            for id in dd_supplier_ids:
                for question in questions:
                    DueDiligenceQuestion.objects.update_or_create(
                        due_diligence_supplier_id=id,
                        question=question.description,
                    )

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


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'Currency')
        fields = ['id', 'name', 'initials']


class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryType')
        fields = ['id', 'name', 'category_group', 'innitials']

        ref_name = "PrequalCategoryTypeSerializer"


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('suppliers', 'Supplier')
        fields = ['id', 'company_name', 'contact_name', 'phone_number', 'email_address']


# class QaSectionQuestionInstructions(serializers.ModelSerializer):
#     qa_questions = serializers.SerializerMethodField()
#
#     class Meta:
#         model = Section
#         fields = ['name', 'description', 'category', 'qa_questions']
#
#     def get_qa_questions(self, obj):
#         qaqs = QualityAssuranceQuestion.objects.filter(question__section_id=obj.id)
#         return QAQSerializer(qaqs, many=True).data

class QuestionSupplierResponseSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()
    supplier_response = serializers.SerializerMethodField()
    section_name = serializers.CharField(read_only=True, source="question.section.name")

    class Meta:
        model = Question

        fields = [
            'id', 'description', 'trans_description', 'section', 'answer_type', 'is_required',
            'max_score', 'is_scored', 'is_qa', 'is_dd', 'options', 'score', 'supplier_response','section_name',
        ]

    def get_options(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.options
        else:
            return ''

    def get_score(self, obj):
        scheme = MarkingScheme.objects.filter(question_id=obj.id).first()
        if scheme is not None:
            return scheme.score
        else:
            return ''

    def get_supplier_response(self, obj):
        supplier_response = SupplierResponse.objects.filter(
            supplier_id=self.context['participant_id'],
            question_id=obj.id
        ).first()
        return SRSerializer(supplier_response, many=False).data


class QAQSupplierResponseSerializer(serializers.ModelSerializer):
    question = serializers.SerializerMethodField()
    qa_question_response = serializers.SerializerMethodField()
    question_type = serializers.SerializerMethodField()
    question_type_response = serializers.SerializerMethodField()

    class Meta:
        model = QualityAssuranceQuestion
        fields = [
            'id', 'question', 'quality_assurance', 'verification_instruction', 'qa_question_response', 'question_type',
            'question_type_response'
        ]

    def get_question(self, obj):
        question = Question.objects.filter(id=obj.question_id).first()
        return QuestionSupplierResponseSerializer(
            question, many=False, context={'participant_id': self.context['participant_id']}).data

    def get_qa_question_response(self, obj):
        qaq_response = QualityAssuranceResponse.objects.filter(
            quality_assurance_question_id=obj.id, supplier_id=self.context['participant_id']
        ).first()
        return QARRetrieveSerializer(qaq_response, many=False).data

    def get_question_type(self, obj):
        if obj.question.short_description.lower() == "Tax compliance".lower():
            question_type = "tcc"
        elif obj.question.short_description.lower() == "Certificate of Incorporation".lower() or \
            obj.question.short_description.lower() == "Registration certificate".lower():
            question_type = "coi"
        elif obj.question.short_description.lower() == "CR12 Certificate or equivalent".lower():
            question_type = "cr12"
        elif obj.question.short_description.lower() == "Pharmacy and Poisons Board License".lower():
            question_type = "ppb"
        elif obj.question.short_description.lower() == "National identification number".lower():
            question_type = "id"
        elif obj.question.short_description.lower() == "PIN certificate".lower():
            question_type = "pin"
        elif obj.question.short_description.lower() == "Business permit".lower():
            question_type = "bp"
        elif obj.question.short_description.lower() == "NCA Registration certificate".lower():
            question_type = "nca_c"
        else:
            question_type = "normal"

        return question_type

    def get_question_type_response(self, obj):
        if obj.question.short_description.lower() == "Tax compliance".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id, short_description="PIN number").first()
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        return supplier_response.options
                    return "No Response Submitted"
                return "No Response Submitted"
            return "No Response Submitted"
        elif obj.question.short_description.lower() == "CR12 Certificate or equivalent".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                short_description="Company registration certificate number").first()
            data = {}
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        data['registration_number'] = supplier_response.options

            directors = []
            d1 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 1"
            ).first()

            d2 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 2"
            ).first()

            d3 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 3"
            ).first()

            d4 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 4"
            ).first()

            d5 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 5"
            ).first()

            d6 = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                description="1. Names of the director or shareholders 6"
            ).first()

            if d1:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            if d2:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            if d3:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            if d4:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            if d5:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            if d6:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=d1.id, supplier_id=self.context['participant_id']).first()
                if supplier_response:
                    directors.append(supplier_response.options)
            data['directors'] = directors
            print(data)
            return data
        elif obj.question.short_description.lower() == "Business permit".lower() or\
                obj.question.short_description.lower() == "Pharmacy and poisons board License".lower():
            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
                id=self.context['participant_id']).first()
            if supplier is not None:
                return supplier.company_name
            return "No Company Name"
        elif obj.question.short_description.lower() == "Registration certificate".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id,
                short_description="Company registration certificate number").first()
            data = {}
            data['registration_number'] = None
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        data['registration_number'] = supplier_response.options

            supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
                id=self.context['participant_id']).first()
            data['company_name'] = None
            if supplier is not None:
                data['company_name'] = supplier.company_name
            print(data)
            return data
        elif obj.question.short_description.lower() == "National identification number".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id, short_description="National identification number").first()
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        return supplier_response.options
                    return "No Response Submitted"
                return "No Response Submitted"
            return "No Response Submitted"
        elif obj.question.short_description.lower() == "PIN certificate".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id, short_description="PIN number").first()
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        return supplier_response.options
                    return "No Response Submitted"
                return "No Response Submitted"
            return "No Response Submitted"
        elif obj.question.short_description.lower() == "NCA certificate".lower():
            q = Question.objects.filter(
                section__category_id=obj.question.section.category_id, short_description="NCA certificate").first()
            if q is not None:
                supplier_response = SupplierResponse.objects.filter(
                    question_id=q.id, supplier_id=self.context['participant_id']).first()
                if supplier_response is not None:
                    if supplier_response.options:
                        return supplier_response.options
                    return "No Response Submitted"
                return "No Response Submitted"
            return "No Response Submitted"
        elif obj.question.section.name.lower() == "Financial Ratios".lower():
            q = Question.objects.filter(
                short_description='Financial statements', section__category_id=obj.question.section.category_id).first()
            if not q:
                return None
            supplier_response = SupplierResponse.objects.filter(
                question_id=q.id, supplier_id=self.context['participant_id']
            ).first()

            if supplier_response is not None:
                if supplier_response.document_url is not None:
                    return supplier_response.document_url
                else:
                    return None
            else:
                return None
        return "No Response Submitted"


class QaSectionQuestionsSupplierResponse(serializers.ModelSerializer):
    qa_questions = serializers.SerializerMethodField()
    ratios_instance = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = ['name', 'description', 'category', 'qa_questions', 'ratios_instance']

    def get_qa_questions(self, obj):
        qaqs = QualityAssuranceQuestion.objects.filter(question__section_id=obj.id)
        return QAQSupplierResponseSerializer(
            qaqs, many=True, context={'participant_id': self.context['participant_id']}).data
    
    def get_ratios_instance(self, obj):
        if obj.name == 'Financial Ratios':
            none = {
                'equity': None, 'curr_liabilities': None, 'fixed_assets': None,
                'current_assets': None, 'debtors': None, 'turnover': None,  'gross_profit': None,
                'net_profit': None, 'cash': None,
                'equity_after_qa': None, 'curr_liabilities_after_qa': None, 'fixed_assets_after_qa': None,
                'current_assets_after_qa': None, 'debtors_after_qa': None, 'turnover_after_qa': None, 'gross_profit_after_qa': None,
                'net_profit_after_qa': None, 'cash_after_qa': None
            }
            instance = FinancialRatio.objects.filter(
                section_id=obj.id, supplier_id=self.context['participant_id']).first()
            if instance is not None:
                return FinancialRatioRetrieveSerializer(instance, many=False).data
            return none
        else:
            return None


class SupplierCategoryScoreSerializer(serializers.ModelSerializer):
    has_award_letter = serializers.SerializerMethodField()
    has_regret_letter = serializers.SerializerMethodField()

    class Meta:
        model = SupplierCategoryScore
        fields = [
            'id', 'score', 'score_after_qa', 'supplier', 'rank', 'rank_after_qa', 'has_award_letter',
            'has_regret_letter'
        ]
        depth = 2

    def get_has_award_letter(self, obj):
        if AwardLetter.objects.filter(supplier_id=obj.supplier_id).count() > 0:
            return True
        return False

    def get_has_regret_letter(self, obj):
        if RegretLetter.objects.filter(supplier_id=obj.supplier_id).count() > 0:
            return True
        return False


class AwardLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AwardLetter
        fields = [
            'id', 'name', 'description', 'supplier', 'category', 'award_date',
            'letter'
        ]


class MultipleAwardLetterSerializer(serializers.Serializer):
    supplier_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['supplier_ids']


class MultipleRegretLetterSerializer(serializers.Serializer):
    supplier_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['supplier_ids']


class MultipleCustomLetterSerializer(serializers.Serializer):
    supplier_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['supplier_ids']


class MultipleDDLetterSerializer(serializers.Serializer):
    supplier_ids = serializers.ListField(child=serializers.IntegerField())

    class Meta:
        fields = ['supplier_ids']


class RegretLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegretLetter
        fields = [
            'id', 'name', 'description', 'supplier', 'category', 'regret_date',
            'letter'
        ]


class CustomLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomLetter
        fields = [
            'id', 'name', 'description', 'supplier', 'category', 'custom_letter_date',
            'letter'
        ]


class DDLetterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DueDilligenceLetter
        fields = [
            'id', 'name', 'description', 'supplier', 'category', 'due_dilligence_letter_date',
            'letter'
        ]


class InviteBidderSerializer(serializers.ModelSerializer):
    emails = serializers.CharField(max_length=30000)

    class Meta:
        model = CategoryInvite
        fields = ['id', 'category', 'emails']

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)
        i = None
        try:
            email_list = validated_data['emails'].split(',')
            for e in email_list:
                supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(email=e).first()
                try:
                    instance, created = ModelClass._default_manager.update_or_create(
                        category=validated_data['category'], email=e, supplier_id=supplier.id if supplier else None
                    )
                    if not i:
                        i = instance
                    if supplier:
                        existing_supplier_email_invite.delay(category_id=instance.category.id, supplier_id=supplier.id)
                    else:
                        non_existent_invites_email.delay(user_email=instance.email, category_id=instance.category.id)
                except Exception as e:
                    capture_exception(e)
                    print(e)
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

        # if many_to_many:
        #     for field_name, value in many_to_many.items():
        #         field = getattr(instance, field_name)
        #         field.set(value)

        return i

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()

        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class CategoryInviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryInvite
        fields = ['id', 'email', 'supplier']
        depth = 2


class PrequalQARatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('prequal', 'FinancialRatio')
        fields = [
            'id', 'supplier','section','equity_after_qa', 'curr_liabilities_after_qa',
            'fixed_assets_after_qa', 'current_assets_after_qa', 'debtors_after_qa', 'turnover_after_qa',
            'gross_profit_after_qa', 'net_profit_after_qa', 'cash_after_qa'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}

        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            submit_financial_ratios_after_qa.delay(instance_id=instance.id)
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

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        submit_financial_ratios_after_qa.delay(instance_id=instance.id)

        # Note that many-to-many fields are set after updating instance.
        # Setting m2m fields triggers signals which could potentially change
        # updated instance and we do not want it to collide with .update()
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance

# class ClientDocumentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClientDocument
#         fields = [
#             'id', 'prequalification', 'document_type', 'tendersure_module', 'body',
#             'authoriser_name', 'authoriser_role', 'header', 'footer', 'signature',
#             'watermark', 'file', 'subject'
#         ]


class QuestionArchiveSerializer(serializers.ModelSerializer):
    supplier_response = serializers.SerializerMethodField()

    class Meta:
        model = Question

        fields = [
            'id', 'short_description', 'supplier_response'
        ]

    def get_supplier_response(self, obj):
        supplier_response = SupplierResponse.objects.filter(
            supplier_id=self.context['supplier_id'],
            question_id=obj.id
        ).first()
        if supplier_response != None:
            return SRDocumentSerializer(supplier_response, many=False).data
        else:
            return None


class FinancialRatioRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('prequal', 'FinancialRatio')
        fields = [
            'equity', 'curr_liabilities', 'fixed_assets', 'current_assets', 'debtors', 'turnover', 
            'gross_profit', 'net_profit', 'cash',
            'equity_after_qa', 'curr_liabilities_after_qa', 'fixed_assets_after_qa',
            'current_assets_after_qa', 'debtors_after_qa', 'turnover_after_qa', 'gross_profit_after_qa',
            'net_profit_after_qa', 'cash_after_qa'
        ]


class FinancialRatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('prequal', 'FinancialRatio')
        fields = [
            'equity_after_qa', 'curr_liabilities_after_qa', 'fixed_assets_after_qa',
            'current_assets_after_qa', 'debtors_after_qa', 'turnover_after_qa', 'gross_profit_after_qa',
            'net_profit_after_qa', 'cash_after_qa'
        ]

    def create(self, validated_data):
        raise_errors_on_nested_writes('create', self, validated_data)

        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)

        try:
            instance = ModelClass._default_manager.create(**validated_data)
            calculate_financial_ratios_after_qa(instance_id=instance.id, user=self.context['request'].user)
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

        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)

        return instance

    def update(self, instance, validated_data):
        raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)

        instance.save()
        calculate_financial_ratios_after_qa(instance_id=instance.id, user=self.context['request'].user)
        
        for attr, value in m2m_fields:
            field = getattr(instance, attr)
            field.set(value)

        return instance


class BroadCastNotificationSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    level = serializers.CharField(max_length=250)
    verb = serializers.CharField(max_length=250)
    description = serializers.CharField(max_length=3000)
    type_class = serializers.CharField(max_length=250, required=False, allow_blank=True)

    class Meta:
        fields = ["job_id", "level", "verb", "description", "type_class"]

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return


class EmailNotificationSerializer(serializers.Serializer):
    job_id = serializers.IntegerField()
    level = serializers.CharField(max_length=250)
    to = serializers.CharField(max_length=250)
    verb = serializers.CharField(max_length=250)
    subject = serializers.CharField(max_length=250)
    content = serializers.CharField(max_length=3000)
    potential_selection = serializers.CharField(max_length=250)
    # files = serializers.ListField(
        # child=serializers.FileField(max_length=100000, allow_empty_file=True, use_url=False), allow_empty=True)
    class Meta:
        fields = ["job_id", "level", "to", "verb", "subject", "content", "potential_selection"]

    def create(self, validated_data):
        return

    def update(self, instance, validated_data):
        return
