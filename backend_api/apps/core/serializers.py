from rest_framework.serializers import ModelSerializer, RelatedField
from rest_framework import serializers
from .models import Notifications, CriteriaCountry, CategoryTypeCriteria
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from apps.core.models import (
    Job, CategoryType
)

UserModel = get_user_model()

from apps.buyer.serializers import CompanyListSerializer

class JobsSerializer(serializers.ModelSerializer):
    sourcing_activity = serializers.CharField(source='sourcing_activity.model')
    company = CompanyListSerializer()

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'unique_reference', 'sourcing_activity', 'target_id']

class LiveJobsSerializer(serializers.ModelSerializer):
    sourcing_activity = serializers.CharField(source='sourcing_activity.model')
    responsive_bidders = serializers.SerializerMethodField()
    company = CompanyListSerializer()

    class Meta:
        model = Job
        fields = ['id', 'company', 'title', 'unique_reference', 'sourcing_activity', 'target_id', 'responsive_bidders']

    def get_responsive_bidders(self, obj):
        return obj.bidders['responsive_bidders']


class UserSerializer(ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = UserModel
        fields = ['id', 'username', 'email']


class ContentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = ['app_label', 'model']


class GenericNotificationRelatedField(RelatedField):

    def to_representation(self, value):
        if isinstance(value, UserModel):
            serializer = UserSerializer(value)
        if isinstance(value, ContentType):
            serializer = ContentTypeSerializer(value)

        return serializer.data


class NotificationSerializer(ModelSerializer):
    recipient = UserSerializer()
    actor = UserSerializer()
    timestamp = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Notifications
        fields = ['id', 'recipient', 'actor', 'target', 'verb', 'level', 'description', 'unread', 'public', 'deleted',
                  'emailed', 'timestamp', 'type_class']

    def create(self, validated_data):
        recipient_data = validated_data.pop('recipient')
        recipient = UserModel.objects.get_or_create(id=recipient_data['id'])
        actor_data = validated_data.pop('actor')
        actor = UserModel.objects.get_or_create(id=actor_data['id'])
        notification = Notifications.objects.create(recipient=recipient[0], actor=actor[0], **validated_data)
        return notification


class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = ['id', 'name']

        ref_name = "CoreCategoryTypeSerializer"
