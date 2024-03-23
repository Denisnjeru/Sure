from django.conf import settings
from django.urls import reverse

from apps.common.utils import send_email

if settings.DEBUG:
    current_site_url = "http://127.0.0.1:8000"
else:
    current_site_url = ""


def buyer_send_default_password_email(user, password):
    """
    Send supplier default email
    """
    email_body = f"Dear {user.first_name}, \n Your Tendersure account has been created successfuly. \n Your username is {user.email} and your default password is {password}"
    data = {
        "email_body": email_body,
        "to_email": user.email,
        "email_subject": "Tendersure Account Created",
    }
    send_email(data)


def buyer_send_signup_email(user, token, password):
    """
    Send supplier signup activation link, plus initial password
    """
    relativeLink = reverse("authentication:verify_email")
    absurl = current_site_url + relativeLink + "?token=" + str(token)
    email_body = f"Dear Buyer, \n Thank you for registering wth us.Your Tendersure account has been created successfuly.\n.Use the link below to verify your email {absurl} \n Use the following credentials to login username:{user.email}, default password:{password}."
    data = {
        "email_body": email_body,
        "to_email": user.email,
        "email_subject": "Tendersure Account Activation",
    }
    send_email(data)
