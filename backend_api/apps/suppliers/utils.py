from email import message
from locale import currency
import threading
import random
import string
import math
from django.urls import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string

from decouple import config
from django import http, apps

if settings.DEBUG:
    current_site_url = config("DEV_SITE_URL")
else:
    current_site_url = config("PROD_SITE_URL")


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        print("Sending emails ....")
        self.email.send(fail_silently=True)


def send_email(data):
    message = data["email_body"]
    email = EmailMessage(
        subject=data["email_subject"],
        message=message,
        to=[data["to_email"]],
    )
    email.attach_alternative(message, "text/html")
    EmailThread(email).start()


def send_default_password_email(user, password):
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


def send_supplier_signup_email(user, token, password):
    """
    Send supplier signup activation link, plus initial password
    :Params:
    :user:
    :token:
    "password:
    """
    relativeLink = reverse("authentication:verify_email")
    absurl = config("FRONTEND_URL") + "/activate-account?token=" + str(token)

    email_subject = "Tendersure: Activate your account"
    message = render_to_string(
        "supplier_activate_account.html",
        {
            "user": user,
            "password": password,
            "absurl": absurl,

        },
    )
    email = EmailMultiAlternatives(email_subject, message, to=[user.email])
    email.attach_alternative(message, "text/html")
    email.send(fail_silently=True)



def generate_order_code():
    code = ''.join((random.sample(string.ascii_uppercase, 5)))

    #confirm order_no does not exist
    category_order = apps.apps.get_model("core", "CategoryOrder").objects.filter(code=code).first()
    if category_order is not None:
        code = generate_order_code()

    return code


def tender_financial_ratio_question_score(supplier, question):
    supplier_responses = apps.apps.get_model("tender", "SupplierResponse").objects.filter(
        supplier_id=supplier.id, question_id=question.id
    )

    score = 0
    question_options = question.options
    response = supplier_responses.filter(question_id=question.id).first()

    ac_question = apps.apps.get_model("tender", "Question").objects.filter(
        description="1. For limited liability companies, attach audited accounts for the last two years, "
                    "for sole proprietors and partnerships, attach your most recent management accounts",
        section__category_id=question.section.category_id
    ).first()

    if ac_question is not None:
        supplier_response = apps.apps.get_model("tender", "SupplierResponse").objects.filter(question_id=ac_question.id, supplier_id=supplier.id).first()
        if supplier_response is None:
            return score
        elif supplier_response is not None:
            if supplier_response.options is None and supplier_response.document_url is None \
                    or len(supplier_response.options) < 1 and not supplier_response.document_url.name:
                return score
            else:
                if response is not None:
                    for option in question_options:
                        start = float(option.split("-", 1)[0])
                        end = float(option.split("-", 1)[1])
                        q_ratio = math.floor(float(response.options) * 10) / 10

                        if start <= q_ratio <= end:
                            my_index = question_options.index(option)
                            s = float(question.scores[my_index])
                            score = s
                            break
                        else:
                            continue
                return score
        else:
            return score
    return score


def prequal_financial_ratio_question_score(supplier, question):
    supplier_responses = apps.apps.get_model("prequal", "SupplierResponse").objects.filter(
        supplier_id=supplier.id, question_id=question.id
    )

    score = 0
    question_options = question.options
    response = supplier_responses.filter(question_id=question.id).first()

    ac_question = apps.apps.get_model("prequal", "Question").objects.filter(
        description="1. For limited liability companies, attach audited accounts for the last two years, "
                    "for sole proprietors and partnerships, attach your most recent management accounts",
        section__category_id=question.section.category_id
    ).first()

    if ac_question is not None:
        supplier_response = apps.apps.get_model("prequal", "SupplierResponse").objects.filter(question_id=ac_question.id, supplier_id=supplier.id).first()
        if supplier_response is None:
            return score
        elif supplier_response is not None:
            if supplier_response.options is None and supplier_response.document_url is None \
                    or len(supplier_response.options) < 1 and not supplier_response.document_url.name:
                return score
            else:
                if response is not None:
                    for option in question_options:
                        start = float(option.split("-", 1)[0])
                        end = float(option.split("-", 1)[1])
                        q_ratio = math.floor(float(response.options) * 10) / 10

                        if start <= q_ratio <= end:
                            my_index = question_options.index(option)
                            s = float(question.scores[my_index])
                            score = s
                            break
                        else:
                            continue
                return score
        else:
            return score
    return score