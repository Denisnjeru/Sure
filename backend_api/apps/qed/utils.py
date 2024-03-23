from django.conf import settings
from django.urls import reverse
from apps.common.utils import get_my_current_site
from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from decouple import config

from apps.common.utils import send_email

if settings.DEBUG:
    current_site_url = "http://127.0.0.1:8000"
else:
    current_site_url = ""


def qed_send_signup_email(user, token, password):
    """
    Send qed user activation link
    :Params:
    :user:
    :token:
    "password:
    """
    relativeLink = reverse("authentication:verify_email")
    current_site_url = get_my_current_site()
    absurl = config("FRONTEND_URL") + "/activate-account?token=" + str(token)

    email_subject = "Tendersure: Activate your QED administrator account"
    message = render_to_string(
        "emails/qed_activate_account.html",
        {
            "user": user,
            "password": password,
            "absurl": absurl,
        },
    )
    email = EmailMultiAlternatives(email_subject, message, to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=True)
