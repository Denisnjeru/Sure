import traceback
import random
import string

from datetime import timezone

from django import apps
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from rest_framework import serializers
from rest_framework.serializers import raise_errors_on_nested_writes
from rest_framework.utils import model_meta

from apps.qed.models import Qed, QedPrivilege, QedRole, QedRolePrivilege
from apps.qed.utils import qed_send_signup_email


class QedPrivilegeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QedPrivilege
        fields = ["id", "title", "description"]


class QedPrivilegeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QedPrivilege
        fields = ["id", "title", "description"]

class QedPrivilegeListSummarySerializer(serializers.ModelSerializer):
    has_privilege = serializers.BooleanField()

    class Meta:
        model = QedPrivilege
        fields = ["id", "title", "description", "has_privilege", "created_at"]

class QedRolePrivilegeSerializer(serializers.ModelSerializer):
    class Meta:
        model = QedRolePrivilege
        fields = ["id", "qed_role", "qed_privilege"]


class QedRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = QedRole
        fields = ["id", "name", "description"]


class QedUserCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Create or Update QED User
    """
    email = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Qed
        fields = [
            "id",
            "qed_role",
            "first_name",
            "last_name",
            "email",
        ]

    def create(self, validated_data):
        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(8)
        )

        instance = self.Meta.model(**validated_data)
        instance.username = validated_data["email"]
        instance.password = make_password(password)
        instance.save()

        # try:
        refresh = RefreshToken.for_user(instance).access_token
        qed_send_signup_email(user=instance, token=refresh, password=password)

        # except Exception as e:
        #     pass

        return instance

class QedUserListSerializer(serializers.ModelSerializer):
    """
    List QED users
    """
    qed_role = QedRoleSerializer()
    class Meta:
        model = Qed
        fields = ["id", "qed_role", "first_name", "last_name", "email", "is_active", "date_joined", "last_login"]


# prequal serializers
class CategoryGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryGroup')
        fields = ['id', 'name']


class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryType')
        fields = ['id', 'name', 'category_group', 'innitials']
        depth = 2
        ref_name = "QEDCategoryTypeSerializer"


class CategoryTypeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryType')
        fields = ['id', 'name', 'category_group', 'innitials']


class CriteriaLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = apps.apps.get_model('core', 'CriteriaCountry')
        fields = ['id', 'name']


class CriteriaCountrySerializer(serializers.ModelSerializer):
    criteria = serializers.SerializerMethodField()

    class Meta:
        model = apps.apps.get_model('core', 'CriteriaCountry')
        fields = ['id', 'name', 'criteria']

    def get_criteria(self, obj):
        c = apps.apps.get_model('core', 'CategoryTypeCriteria').objects.filter(
            category_type_id=self.context['category_type_id'], criteria_country_id=obj.id
        ).first()
        if c is not None:
            return CategoryTypeCriteriaSerializer(c, many=False).data
        else:
            return 'No criteria available'


class CategoryTypeCriteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryTypeCriteria')
        fields = ['id', 'criteria_country', 'category_type', 'file_url']
        depth = 2


class CategoryTypeCriteriaCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.apps.get_model('core', 'CategoryTypeCriteria')
        fields = ['id', 'criteria_country', 'category_type', 'file_url']


class CategoryTypeSupplierUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    class Meta:
        fields = ['file',]

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
