import random
import string

from django.contrib.auth.hashers import make_password

from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework import serializers
from apps.buyer.utils import buyer_send_default_password_email, buyer_send_signup_email
from .models import Company, Buyer, BuyerRole, BuyerPrivilege, BuyerRolePrivilege


class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "company_name",
            "contact_name",
            "phone_number",
            "kra_pin_number",
            "buyer_initials",
            "company_logo_url",
        ]


class CompanyCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "company_name",
            "phone_number",
            "contact_name",
            "country",
            "buyer_initials",
            "kra_pin_number",
            "company_logo_url",
        ]

    def validate(self, attrs):
        kra_pin_number = attrs.get("kra_pin_number", "")
        phone_number = attrs.get("phone_number", "")

        if Company.objects.filter(kra_pin_number=kra_pin_number).exists():
            raise serializers.ValidationError(
                {
                    "kra_pin_number": "A buyer account with tha Tax pin number already exists"
                }
            )
        if Company.objects.filter(phone_number=phone_number).exists():
            raise serializers.ValidationError(
                {"phone_number": "A buyer with that phone number already exists"}
            )

        return super().validate(attrs)

    def create(self, validated_data):
        instance = self.Meta.model(**validated_data)
        instance.save()

        return instance

    def update(self, instance, validated_data):
        pass


class BuyerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Buyer
        fields = [
            "id", "company", "buyer_role", "first_name", "last_name", "email", "is_active", "date_joined",
            "last_login"
        ]
        depth = 2


class BuyerCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Create,Update Company Users
    """

    email = serializers.CharField(max_length=100, required=True)

    class Meta:
        model = Buyer
        fields = [
            "id",
            "buyer_role",
            "first_name",
            "last_name",
            "email",
        ]

    def create(self, validated_data):
        password = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(8)
        )

        # company = validated_data.get("company", None)
        # buyer_role = validated_data.get("buyer_role", None)
        # company=self.context["request"].auth.payload["company_id"]
        if "company_id" in self.context["request"].session:
            company = self.context["request"].session["company_id"]
        else:
            view = self.context.get("view")
            company = view.kwargs["company_id"]

        instance = self.Meta.model(**validated_data)
        instance.username = validated_data["email"]
        instance.company_id = company
        instance.password = make_password(password)
        instance.save()

        try:
            refresh = RefreshToken.for_user(instance).access_token
            buyer_send_signup_email(user=instance, token=refresh, password=password)

        except Exception as e:
            pass

        return instance


class BuyerRoleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRole
        fields = ["id", "name", "description", "created_at", "company"]


class BuyerRoleCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRole
        fields = ["id", "name", "description"]

    def create(self, validated_data):
        if "company_id" in self.context["request"].session:
            company = self.context["request"].session["company_id"]
        else:
            view = self.context.get("view")
            company = view.kwargs["company_id"]

        instance = self.Meta.model(**validated_data)
        instance.company_id = company_id
        # if company is not None:
        #     company_obj = Company.objects.get(id=company)
        #
        # instance.company = company_obj
        instance.save()

        return instance


class BuyerPrivilegeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPrivilege
        fields = ["id", "title", "description"]

class BuyerPrivilegeListSummarySerializer(serializers.ModelSerializer):
    has_privilege = serializers.BooleanField()

    class Meta:
        model = BuyerPrivilege
        fields = ["id", "title", "description", "has_privilege", "created_at"]

class BuyerPrivilegeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerPrivilege
        fields = ["id", "title", "description"]


class BuyerRolePrivilegeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRolePrivilege
        fields = ["id", "buyer_role", "buyer_privilege"]


class BuyerRolePrivilegeCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BuyerRolePrivilege
        fields = ["id", "buyer_role", "buyer_privilege"]
