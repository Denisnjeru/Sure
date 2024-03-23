import datetime
from multiprocessing import context
import os
from pathlib import Path
from celery import shared_task
from django.apps import apps
from django.template.loader import render_to_string
from django.core.mail import (
    EmailMultiAlternatives,
    EmailMessage,
    get_connection,
    message,
)
import requests
from apps.common.utils import get_local_filepath

from apps.rfq.models import Category, RfqInvitee, SupplierResponse


@shared_task(bind=True)
def send_participation_acknowledgment(self,supplier_id, category_id, created=False):
    """
    Send the supplier email, to acknowledge submission of RFQ
    :param supplier_id:
    :param categrory_id:
    :return:
    """
    category = Category.objects.filter(id=category_id).first()
    supplier = (
        apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
    )

    if category is not None and supplier is not None:
        try:
            email_subject = (
                "Tendersure: RFQ Participation: %s " % category.name.title()
            )
            if created:
                body = render_to_string(
                    "emails/rfq_participation_acknowledgment.html",
                    {
                        "category": category,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )
            else:
                body = render_to_string(
                    "emails/rfq_response_update.html",
                    {
                        "category": category,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )

            email = EmailMultiAlternatives(
                subject=email_subject, body=body, to=[supplier.email_address]
            )
            email.attach_alternative(body, "text/html")
            email.send()
            print(f"email send successfuly to {supplier.email_address}")

            context = {"success": "email sent successfuly"}
            return context
        except Exception as e:
            print(e)
            #cature exception
    else:
        context = {"error": "Category or Supplier is None"}
        return context


@shared_task(bind=True)
def send_financial_responses(self,category_id):
    """
    Sends the supplier PDF response of their RFQ submission
    :param category_id:
    "param supplier_id:
    :return:
    """
    try:
        category = Category.objects.filter(id=category_id).first()
        suppliers = category.participants["participants"]

        for supplier in suppliers:
            if supplier is not None and category is not None:
                rfq_response = SupplierResponse.objects.filter(
                    supplier=supplier, category=category
                ).first()

                email_subject = "Tendersure: Your RFQ Participation Responses: %s " % category.name

                body = render_to_string(
                    "emails/rfq_responses_body.html",
                    {
                        "category": category,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )

                if rfq_response.document_url:
                    time = datetime.datetime.now()
                    # A = PrivateMediaStorage()
                    # headers = {"ResponseContentDisposition": f"attachment;"}

                    # file_url = A.url(
                    #     f"",
                    #     expire=300,
                    #     parameters=headers,
                    #     http_method="GET",
                    # )
                    # file_url = rfq_response.document_url.url
                    # dir_name = Path(
                    #     "media/temp/{}/{}/{}".format(time.year, time.month, time.day)
                    # )  # folder structure
                    # dir_name.mkdir(parents=True, exist_ok=True)
                    # file_name = rfq_response.document_url.name
                    # filepath = "{}/{}".format(dir_name, file_name)
                    filepath = get_local_filepath(rfq_response.document_url.url)
                    print(filepath)
                    # r = requests.get(file_url)
                    # with open("{}".format(filepath), "wb") as f:
                    #     f.write(r.content)

                    email = EmailMultiAlternatives(
                        subject=email_subject, body=body, to=[supplier.email_address]
                    )
                    email.attach_alternative(body, "text/html")
                    email.attach_file(filepath)
                    email.send()
                    context = {"success": "email sent successfuly"}
                    return context
                else:
                    context = {"error": "No responses"}
                    return context

    except Exception as e:
        print(e)
        context = {"error": "Invalid email address"}
        return context

def send_rfq_category_emails(category_id, type=None):
    """
    Send RFQ Category Reminder & Extensio Emails
    :param: category_id:
    :param: type <str>:
    """
    category = Category.objects.filter(id=category_id).first()

    if category is not None:
        invitees = RfqInvitee.objects.filter(category=category)
        not_sent = []
        for supplier in invitees:
            if type == "reminder":
                email_subject = f"{category.name.title()} Reminder"
                body = render_to_string(
                    "emails/rfq_reminder.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": category.rfq.company.company_name,
                        "category": category,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "company_logo",
                        "phone_number": "+254709557000",
                    },
                )
            elif type == "extension":
                email_subject = f"{category.name.title()} Extension"
                body = render_to_string(
                    "emails/rfq_extension.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": category.rfq.company,
                        "category": category,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "company_logo",
                        "phone_number": "+254709557000",
                    },
                )
            else:
                pass

            try:
                email = EmailMultiAlternatives(
                    subject=email_subject,
                    body=body,
                    to=[supplier.email],
                )
                email.attach_alternative(body, "text/html")
                email.send(fail_silently=True)
                result = {"message": "True"}
            except Exception as e:
                print(f"Exception {e} ")
                not_sent.append(supplier.email)
                result = {"message": "False", "failed": not_sent}
    else:
        pass
        
    context = {"message":"success", "status":200}
    return context


