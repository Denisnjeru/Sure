from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


from .views import (
    MyTokenObtainPairView,
    PasswordTokenCheckAPI,
    RequestAccountActivationView,
    RequestPasswordResetEmail,
    SetNewPasswordAPIView,
    UserLoginAPIView,
    UserLogoutAPIView,
    VerifyEmailView,
    UserLogView,
    VerificationCodeView
)


app_name = "authentication"
router = DefaultRouter()
router.register(r'user_logs', UserLogView, basename='user_log')
router.register(r'tfa', VerificationCodeView, basename='tfa')

urlpatterns = [
    path('', include((router.urls, 'authentication'), namespace='authentication')),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "token",
        MyTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("login", UserLoginAPIView.as_view(), name="login"),
    path("logout", UserLogoutAPIView.as_view(), name="logout"),
    path("verify_email", VerifyEmailView.as_view(), name="verify_email"),
    path(
        "request-reset-email/",
        RequestPasswordResetEmail.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordTokenCheckAPI.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
    path(
        "account/activation/",
        RequestAccountActivationView.as_view(),
        name="request_account_activation",
    ),
]
