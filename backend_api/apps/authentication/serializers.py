from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from axes.utils import reset

from apps.authentication.models import User, UserVisit, VerificationCode
from apps.authentication.tokens import MyTokenObtainPairSerializer
from apps.authentication.utils import send_two_factor_verification_email, generate_verification_code
from apps.buyer.models import Buyer
from apps.suppliers.models import Supplier


def get_user_type(user_id):
    if Supplier.objects.filter(id=user_id).exists():
        user_type = "supplier"
    elif Buyer.objects.filter(id=user_id).exists():
        user_type = "buyer"
    else:
        user_type = "qed"

    return user_type


class UserLoginSerializer(serializers.ModelSerializer, MyTokenObtainPairSerializer):
    """
    User Login
    """

    username = serializers.CharField(max_length=100, min_length=3)
    password = serializers.CharField(max_length=20, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["username", "password"]

    def validate(self, attrs):
        username = attrs.get("username", "")
        password = attrs.get("password", "")

        user = auth.authenticate(username=username, password=password, request=self.context["request"])

        if not user:
            raise AuthenticationFailed("Invalid user credentials")
        if not user.is_active:
            raise AuthenticationFailed("User account disabled, activate your account")

        data = super().validate(attrs)

        refresh = self.get_token(user)

        user_type = get_user_type(user.id)

        if user_type != 'supplier':
            verification_code = generate_verification_code()
            VerificationCode.objects.update_or_create(
                user_id=user.id,
                defaults={
                    "code": verification_code,
                    "user_id": user.id
                }
            )
            # send_two_factor_verification_email.delay(user, verification_code)

        data["refresh"] = str(refresh)

        return data


class UserEmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ["token"]


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    redirect_url = serializers.CharField(max_length=500, required=False)

    class Meta:
        fields = ["email"]


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        # try:
        password = attrs.get("password")
        token = attrs.get("token")
        uidb64 = attrs.get("uidb64")

        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            raise AuthenticationFailed("The password reset link is invalid", 401)

        user.set_password(password)
        user.save()
        reset(username=user.username)
        return user

        # except Exception as e:
        #     raise AuthenticationFailed("The reset link is invalid", 401)

        return super().validate(attrs)


class UserLogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail("bad_token")

class RequestAccountActivationSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email"]

class UserVisitSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserVisit
        fields = ['id', 'user', 'url', 'remote_addr', 'created_at']

class VerificationCodeSerializer(serializers.ModelSerializer):

    class Meta:
        model = VerificationCode
        fields = ['code']
