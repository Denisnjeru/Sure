from email import message
from locale import currency
import threading
import random
import string
import os

from django.urls import reverse
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from datetime import datetime, timedelta, date
from celery import shared_task
from decouple import config
from django import http, apps

from apps.core.utils import weasy_pdf
from django.template.loader import render_to_string, get_template
from pathlib import Path
from apps.payments.tasks import save_payment_receipt

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


def send_mpesa_receipt_email(stk_response, supplier, categories):
    """
    Send payment receipt for zero charge categories.
    :Params:
    :user:
    :token:
    "password:
    """

    """ Send Payment Acknowledgement"""
    time = datetime.now()
    file_path = 'media/payment_receipts/%s' % supplier.company_name.replace(' ', '_')
    filename = "%s_%d_%d.pdf" % (supplier.company_name.replace(' ', '_'), time.year, time.month)
    Path(file_path).mkdir(parents=True, exist_ok=True)
    template_path = os.path.join(settings.BASE_DIR + '/apps/payments/templates/payments/receipt.html')
    payment_ref = stk_response.mpesa_confirmation_code
    context = {
        'company_name': supplier.company_name, 'phone_number': stk_response.phone_number, 'name': f"{supplier.first_name} {supplier.last_name}",
        'total': total,
        'payment_confirmation': stk_response.mpesa_confirmation_code,
        'currency': categories[0].currency.name,
        'categories': categories, 'date': datetime.now()
    }
    pdf_file_path = weasy_pdf(template_src=template_path, context_dict=context, file_name=filename, file_path=file_path)

    try:
        mode_of_payment = "MPESA"
        save_receipt = save_payment_receipt.delay(
            filepath=pdf_file_path,
            filename=filename,
            supplier_id=supplier.id,
            mode_of_payment=mode_of_payment,
            reference=payment_ref,
            amount=0,
            payment_date=datetime.now(),
        )
    except Exception as e:
        capture_exception(e)

    email_subject = 'Acknowledging of Mpesa Payment'
    amount = stk_response.amount
    body = render_to_string('payments/payment_email.html', {
        'supplier': supplier,
        'order_number': stk_response.reference,
        'paid_amount': stk_response.amount,
        'categories': categories,
        'total': total,
        'mode_of_payment': 'Mpesa',
        'currency': categories[0].currency
    })

    message = render_to_string('payments/payment_email.html', {
        'supplier': supplier,
        'order_number': stk_response.reference,
        'paid_amount': stk_response.amount,
        'categories': categories,
        'total': total,
        'mode_of_payment': 'Mpesa',
        'currency': categories[0].currency.name
    })

    email = EmailMultiAlternatives(subject=email_subject, body=body, to=[supplier.email])
    email.attach_alternative(message, "text/html")
    email.attach_file(pdf_file_path)
    email.send(fail_silently=True)

# @shared_task(bind=True)
def send_zero_charge_success_email(supplier, categories, payment_ref):
    """
    Send payment receipt for zero charge categories.
    :Params:
    :user:
    :token:
    "password:
    """

    """ Send Payment Acknowledgement"""
    time = datetime.now()
    file_path = 'media/payment_receipts/%s' % supplier.company_name.replace(' ', '_')
    filename = "%s_%d_%d.pdf" % (supplier.company_name.replace(' ', '_'), time.year, time.month)
    Path(file_path).mkdir(parents=True, exist_ok=True)
    template_path = os.path.join(settings.BASE_DIR + '/apps/payments/templates/payments/receipt.html')

    context = {
        'company_name': supplier.company_name, 'phone_number': supplier.phone_number, 'name': f"{supplier.first_name} {supplier.last_name}",
        'total': 0,
        'payment_confirmation': '',
        'currency': categories[0].currency.name,
        'categories': categories, 'date': datetime.now()
    }
    pdf_file_path = weasy_pdf(template_src=template_path, context_dict=context, file_name=filename, file_path=file_path)


    try:
        mode_of_payment = "FREE"
        save_receipt = save_payment_receipt.delay(
            filepath=pdf_file_path,
            filename=filename,
            supplier_id=supplier.id,
            mode_of_payment=mode_of_payment,
            reference=payment_ref,
            amount=0,
            payment_date=datetime.now(),
        )
    except Exception as e:
        capture_exception(e)

    email_subject = 'Acknowledging of Category Access'
    amount = 0
    body = render_to_string('payments/payment_email.html', {
        'supplier': supplier,
        'order_number': payment_ref,
        'paid_amount': 0,
        'categories': categories,
        'total': 0,
        'mode_of_payment': 'FREE',
        'currency': categories[0].currency
    })

    message = render_to_string('payments/payment_email.html', {
        'supplier': supplier,
        'order_number': payment_ref,
        'paid_amount': 0,
        'categories': categories,
        'total': 0,
        'mode_of_payment': 'FREE',
        'currency': categories[0].currency.name
    })

    email = EmailMultiAlternatives(subject=email_subject, body=body, to=[supplier.email])
    email.attach_alternative(message, "text/html")
    email.attach_file(pdf_file_path)
    email.send(fail_silently=True)

def send_dpo_receipt_email(supplier, dpo_payment):
    name = dpo_payment.customer_name
    phone_number = dpo_payment.customer_phone
    amount = dpo_payment.transaction_amount
    reference = dpo_payment.reference

    orders = CategoryOrder.objects.filter(
        Q(category__status_open=True) | Q(asset_disposal_category__status_open=True),
        code=reference,
    )
    currency = orders.first().category.currency
    time = datetime.now()
    file_path = "media/payment_receipts/%s" % supplier.company_name.replace(" ", "_")
    filename = "%s_%d_%d.pdf" % (
        supplier.company_name.replace(" ", "_"),
        time.year,
        time.month,
    )
    Path(file_path).mkdir(parents=True, exist_ok=True)

    template_path = os.path.join(
        BASE_DIR + "/apps/payments/templates/payments/dpo/receipt.html"
    )

    user = User.objects.filter(id=supplier.user_ptr_id)
    categories = Category.objects.filter(
        id__in=orders.only("category_id").values("category_id")
    )

    context = {
        "user": user,
        "payment": dpo_payment,
        "total": amount,
        "name": f"{name}",
        "phone_number": phone_number,
        "company_name": supplier.company_name,
        "categories": categories,
        "date": datetime.now(),
    }

    pdf_file_path = weasy_pdf(
        template_src=template_path,
        context_dict=context,
        file_name=filename,
        file_path=file_path,
    )

    try:
        mode_of_payment = "DPO"
        save_receipt = save_payment_receipt.delay(
            filepath=pdf_file_path,
            filename=filename,
            supplier_id=supplier.id,
            mode_of_payment=mode_of_payment,
            reference=reference,
            amount=amount,
            payment_date=datetime.datetime.now(),
        )
    except Exception as e:
        capture_exception(e)

    email_subject = "Acknowledging of Payment"
    amount = amount
    body = render_to_string(
        "payments/dpo/email.html",
        {
            "supplier": supplier,
            "order_number": reference,
            "paid_amount": amount,
            "categories": categories,
            "total": amount,
            "currency": currency,
        },
    )

    message = render_to_string(
        "payments/dpo/email.html",
        {
            "supplier": supplier,
            "order_number": reference,
            "paid_amount": amount,
            "categories": categories,
            "total": amount,
            "currency": currency,
        },
    )

    email = EmailMultiAlternatives(
        subject=email_subject, body=body, to=[supplier.email]
    )
    email.attach_alternative(message, "text/html")
    email.attach_file(pdf_file_path)
    email.send()
    return True