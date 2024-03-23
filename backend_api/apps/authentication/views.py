from email import message
import jwt

from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse
from axes.decorators import axes_dispatch
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics, status, views, permissions, viewsets
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import pagination
from rest_framework.decorators import action

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from decouple import config

from apps.authentication.models import User
from apps.authentication.serializers import (
    RequestAccountActivationSerializer,
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
    UserEmailVerificationSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserVisitSerializer,
    VerificationCodeSerializer,
)
from apps.authentication.tokens import MyTokenObtainPairSerializer
from apps.authentication.utils import send_user_account_activation_email, user_send_password_reset_email, send_two_factor_verification_email, generate_verification_code
from apps.common.utils import get_my_current_site
from apps.authentication.serializers import UserVisitSerializer
from apps.authentication.models import UserVisit, VerificationCode
from apps.core.pagination import PageNumberPagination

@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class MyTokenObtainPairView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """

    serializer_class = MyTokenObtainPairSerializer

@method_decorator(axes_dispatch, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class UserLoginAPIView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # request.session["company_id"] = data["company_id"]
        return Response(data, status=status.HTTP_200_OK)


class VerifyEmailView(views.APIView):
    serializer_class = UserEmailVerificationSerializer

    # token_param_config = openapi.Parameter(
    #     "token",
    #     in_=openapi.IN_QUERY,
    #     description="Description",
    #     type=openapi.TYPE_STRING,
    # )

    # @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get("token")
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")
            user = User.objects.get(id=payload["user_id"])
            if not user.is_active:
                user.is_active = True
                user.save()

            # redirect_url = settings.FRONTEND_URL + "/login"

            # #{"email": "Successfully activated"}, status=status.HTTP_200_OK
            # return redirect(redirect_url)
            return Response(
                {"success": "Activation activated successfully"}, status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError as identifier:
            return Response(
                {"error": "Activation expired"}, status=status.HTTP_400_BAD_REQUEST
            )
        except jwt.exceptions.DecodeError as identifier:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
            )


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            # relativeLink = reverse(
            #     "authentication:password-reset-confirm",
            #     kwargs={"uidb64": uidb64, "token": token},
            # )

            # redirect_url = request.data.get("redirect_url", "")
            # current_site_url = get_my_current_site()
            # abs_url = current_site_url + relativeLink

            abs_url = config("FRONTEND_URL") + "/set-password/" + uidb64 + "/" + token
            user_send_password_reset_email(user.email, abs_url)
        return Response(
            {"success": "We have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get("redirect_url")

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            # if not PasswordResetTokenGenerator().check_token(user, token):
            #     return Response({"error": "Token is not valiid"})
            # return Response(
            #     {
            #         "success": True,
            #         "message": "Credentials Valid",
            #         "uidb64": uidb64,
            #         "token": token,
            #     }
            # )
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            else:
                return Response(
                    {"success": "Token is valid"},
                    status=status.HTTP_200_OK,
                )

            # if not PasswordResetTokenGenerator().check_token(user, token):
            #     if len(redirect_url) > 3:
            #         # return redirect(f"{redirect_url}?token_valid=False")
            #         return Response(
            #             {"error": "Token is not valid, please request a new one"},
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )
            #     else:
            #         # return redirect(f"{settings.FRONTEND_URL}?token_valid=False")
            #         return Response(
            #             {"error": "Token is not valid, please request a new one"},
            #             status=status.HTTP_400_BAD_REQUEST,
            #         )

            # if redirect_url and len(redirect_url) > 3:
            #     # return redirect(
            #     #     f"{redirect_url}?token_valid=True&message=Credentials Valid&uidb64={uidb64}&token={token}"
            #     # )
            #     return Response(
            #         {"success": "Token is valid"},
            #         status=status.HTTP_200_OK,
            #     )
            # else:
            #     # return redirect(f"{settings.FRONTEND_URL}?token_valid=False")
            #     return Response(
            #         {"error": "Token is not valid, please request a new one"},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return Response(
                        {"error": "Token is not valid, please request a new one"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
                    # return redirect(f"{redirect_url}?token_valid=False")

            except UnboundLocalError as e:
                return Response(
                    {"error": "Token is not valid, please request a new one"},
                    status=status.HTTP_400_BAD_REQUEST,
                )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": "Password reset successfully"},
            status=status.HTTP_200_OK,
        )


class UserLogoutAPIView(generics.GenericAPIView):
    # permission_classes = (permissions.IsAuthenticated,)

    serializer_class = UserLogoutSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {"message": "User logged out"}, status=status.HTTP_204_NO_CONTENT
        )

class RequestAccountActivationView(generics.GenericAPIView):
    """
    User Request account activation
    Redirects to login if account active (status=active), else sends activation email
    """
    serializer_class = RequestAccountActivationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data.get("email", "")

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            if user.is_active:
                redirect_url = settings.FRONTEND_URL + "/login"
                return redirect(f"{redirect_url}?status=active")
            else:
                refresh = RefreshToken.for_user(user).access_token

                send_user_account_activation_email.delay(user=user, token=refresh)
                return Response(
                    {"message": "We have sent you a link to activate your account"},
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": "A user with that email does not exist"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

class UserLogView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get',]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return UserVisit.objects.filter(user_id=self.request.auth.payload['user_id']).order_by('-id')

    def get_serializer_class(self):
        return UserVisitSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

class VerificationCodeView(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    http_method_names = ['get', 'post']
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return VerificationCode.objects.filter(user_id=self.request.auth.payload['user_id']).order_by('-id')

    def get_serializer_class(self):
        return VerificationCodeSerializer

    @action(methods=['get'], detail=False, url_path='resend')
    def resend_code(self, request):
        user = User.objects.filter(user_id=self.request.auth.payload['user_id']).first()
        verification_code = generate_verification_code()
        VerificationCode.objects.update_or_create(
            user_id=user.id,
            defaults={
                "code": verification_code,
                "user_id": user.id
            }
        )
        send_two_factor_verification_email.delay(user, verification_code)
        context = {
                "success": "Verification code has been resent",
            }
        return Response(context, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=False, url_path='verify')
    def verify_code(self, request):
        s = serializers.VerificationCodeSerializer(data=request.data)

        if s.is_valid():
            verification = VerificationCode.objects.filter(user_id=self.request.auth.payload['user_id'], code=request.data.code).first()
            print(verification)
            context = {
                "success": "Verification successful",
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "error": "Invalid or expired code",
            }
            return Response(context, status=status.HTTP_401_UNAUTHORIZED)