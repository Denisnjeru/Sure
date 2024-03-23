import random
from celery import shared_task
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from decouple import config

from apps.common.utils import get_my_current_site
from apps.authentication.models import VerificationCode



# @shared_task(bind=True)
def user_send_password_reset_email(user_email, abs_url, *args, **kwargs):
    """
    Send user reset password emailS
    """
    absurl= f"{abs_url}"

    email_subject = "Tendersure: Reset your password"
    message = render_to_string(
        "emails/user_reset_password.html",
        {
            "absurl": absurl,

        },
    )
    email = EmailMultiAlternatives(email_subject, message, to=[user_email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=True)

@shared_task(bind=True)
def send_user_account_activation_email(self, user, token, *args, **kwargs):
    """
    Send user activation activation link
    :Params:
    :user:
    :token:
    "password:
    """
    relativeLink = reverse("authentication:verify_email")
    current_site_url = get_my_current_site()
    absurl = config("FRONTEND_URL") + "/activate-account?token=" + str(token)

    email_subject = "Tendersure: Activate your account"
    message = render_to_string(
        "emails/activate_account.html",
        {
            "user": user,
            "absurl": absurl,

        },
    )
    email = EmailMultiAlternatives(email_subject, message, to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=True)

@shared_task(bind=True)
def send_two_factor_verification_email(self, user_id, verification_code, *args, **kwargs):
    """
    Send two factor authentication verification code
    :Params:
    :user:
    :verification_code:
    """
    user = User.objects.filter(id=user_id).first()
    email_subject = "Tendersure: Verification Code"
    message = render_to_string(
        "emails/two_factor_auth.html",
        {
            "user": user,
            "verification_code": verification_code,

        },
    )
    email = EmailMultiAlternatives(email_subject, message, to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=True)

def generate_verification_code():
    code = random.randint(10000,99999)

    #confirm order_no does not exist
    verification = VerificationCode.objects.filter(code=code).first()
    if verification is not None:
        code = generate_verification_code()

    return code