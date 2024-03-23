from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType

from apps.contract.models import *
from apps.suppliers.models import Supplier
from apps.buyer.models import Company
from apps.prequal.models import Category
from apps.core.models import Job
from apps.buyer.serializers import CompanyListSerializer
from apps.suppliers.serializers import SupplierListSerializer
from apps.prequal.serializers import CategoryListSerializer
from apps.core.serializers import JobsSerializer

class CategorySupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategorySupplier

class ContractSectionsCombineSerializer(serializers.Serializer):
    source_list = serializers.ListField(required=False, child=serializers.IntegerField())
    content = serializers.CharField(allow_blank=True, required=False)

class SupplierContractListSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='supplier.company_name')
    contact_person = serializers.CharField(source='supplier.contact_name')
    phone_number = serializers.CharField(source='supplier.phone_number')
    created_by = serializers.CharField(source='created_by.email')

    class Meta:
        model = SupplierContract
        fields = ['id', 'name', 'contact_person', 'phone_number', 'start_date', 'end_date', 'status', 'approval_status', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

class SupplierContractRetrieveSerializer(serializers.ModelSerializer):
    supplier = SupplierListSerializer()
    category = CategoryListSerializer()
    live_editor = serializers.SerializerMethodField()

    class Meta:
        model = SupplierContract
        fields = ['id', 'supplier', 'category', 'start_date', 'end_date', 'live_edit', 'live_editor', 'contact_emails', 'content']
        read_only_fields = ('id', 'created_by',)

    def get_live_editor(self, obj):
        if obj.live_editor != None:
            return obj.live_editor.email
        else:
            return None

class SupplierContractSaveSerializer(serializers.Serializer):
    type = serializers.CharField()
    content = serializers.CharField()

    class Meta:
        fields = ['type', 'content']
        read_only_fields = ('id', 'created_by',)

class SupplierContractSerializer(serializers.ModelSerializer):
    source = serializers.CharField(required=False)
    source_list = serializers.ListField(required=False, child=serializers.IntegerField())

    class Meta:
        model = SupplierContract
        fields = ['id', 'supplier', 'category', 'start_date', 'end_date', 'contact_emails', 'source', 'source_list']
        read_only_fields = ('id', 'created_by',)

class ContractCreateSerializer(serializers.ModelSerializer):
    source = serializers.CharField(required=False)
    source_list = serializers.ListField(required=False, child=serializers.IntegerField())
    contract_with = serializers.CharField(required=False)
    contract_for = serializers.CharField(required=False)
    document = serializers.FileField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Contract
        fields = ['id', 'contract_with', 'entity_id', 'contract_for', 'target_id', 'start_date', 'end_date', 'contact_emails', 'content', 'document', 'source', 'source_list']
        read_only_fields = ('id', 'created_by',)

class ContractUpdateSerializer(serializers.ModelSerializer):
    document = serializers.FileField(required=False)
    content = serializers.CharField(required=False)

    class Meta:
        model = Contract
        fields = ['id', 'start_date', 'end_date', 'contact_emails', 'content', 'document']
        read_only_fields = ('id', 'created_by',)

class ContractRevisionsSerializer(serializers.ModelSerializer):
    editor = serializers.CharField(source='editor.email')

    class Meta:
        model = ContractRevisions
        fields = ['id', 'editor', 'changes', 'created_at', 'updated_at']


class ContractRetrieveSerializer(serializers.ModelSerializer):
    entity = serializers.SerializerMethodField()
    target = serializers.SerializerMethodField()
    live_editor = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    approval_status = serializers.SerializerMethodField()
    revisions = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['id', 'entity', 'target', 'contact_emails', 'start_date', 'end_date', 'status', 'approval_status', 'document', 'content', 'live_edit', 'live_editor', 'created_by', 'revisions', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

    def get_entity(self, obj):
        if obj.contract_with.model == 'supplier':
            supplier = Supplier.objects.filter(id=obj.entity_id).first()
            return SupplierListSerializer(supplier).data
        elif obj.contract_with.model == 'company':
            company = Company.objects.filter(id=obj.entity_id).first()
            return CompanyListSerializer(company).data
        else:
            return None

    def get_target(self, obj):
        if obj.contract_for.model == 'category':
            category = Category.objects.filter(id=obj.target_id).first()
            return CategoryListSerializer(category).data
        elif obj.contract_for.model == 'job':
            job = Job.objects.filter(id=obj.target_id).first()
            return JobsSerializer(job).data
        else:
            return None

    def get_live_editor(self, obj):
        if obj.live_editor != None:
            return obj.live_editor.email
        else:
            return None

    def get_status(self, obj):
        return obj.get_status_display()

    def get_approval_status(self, obj):
        return obj.get_approval_status_display()

    def get_revisions(self, obj):
        revisions = ContractRevisions.objects.filter(contract_id=obj.id, live_edit=False)
        return ContractRevisionsSerializer(revisions, many=True).data

class ContractSerializer(serializers.ModelSerializer):
    target = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()
    approval_status = serializers.SerializerMethodField()

    class Meta:
        model = Contract
        fields = ['id', 'document', 'target', 'contact_emails', 'start_date', 'end_date', 'status', 'approval_status', 'live_edit', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

    def get_target(self, obj):
        if obj.contract_for.model == 'category':
            category = Category.objects.filter(id=obj.target_id).first()
            return CategoryListSerializer(category).data
        elif obj.contract_for.model == 'job':
            job = Job.objects.filter(id=obj.target_id).first()
            return JobsSerializer(job).data
        else:
            return None

    def get_status(self, obj):
        return obj.get_status_display()

    def get_approval_status(self, obj):
        return obj.get_approval_status_display()

class ContractSectionListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email')

    class Meta:
        model = ContractSection
        fields = ['id', 'name', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

class ContractSectionSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ContractSection
        fields = ['id', 'name', 'content', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

    def save(self, **kwargs):
        """Include default for read_only `created_by` field"""
        print(self.fields["created_by"].get_default())
        kwargs["created_by"] = self.fields["created_by"].get_default()
        return super().save(**kwargs)

class ContractTemplateListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by.email')

    class Meta:
        model = ContractTemplate
        fields = ['id', 'name', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

class ContractTemplateSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = ContractTemplate
        fields = ['id', 'name', 'content', 'created_by', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_by',)

    def save(self, **kwargs):
        """Include default for read_only `created_by` field"""
        print(self.fields["created_by"].get_default())
        kwargs["created_by"] = self.fields["created_by"].get_default()
        return super().save(**kwargs)

class ContractDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractDocument

class SupplierContractRevisionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupplierContractRevisions
        fields = '__all__'
