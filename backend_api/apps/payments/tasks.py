import datetime
from email import message
import os
from pathlib import Path
from unicodedata import category
from django import apps
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives

from celery import Task, shared_task
from celery_progress.backend import ProgressRecorder
from backend.celery import app

from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from sentry_sdk import capture_exception
from apps.common.utils import get_local_filepath
from apps.core.utils import format_excel, insert_image
from apps.suppliers.models import Supplier
from apps.core.models import SupplierReceipt

@shared_task(bind=True)
def save_payment_receipt(
    self,
    filepath,
    filename,
    supplier_id,
    mode_of_payment,
    reference,
    amount,
    payment_date,
):
    """
    Save supplier receipt to SupplieReceipt model
    """
    if supplier_id is not None:
        supplier = Supplier.objects.filter(id=supplier_id).first()

    if filepath is not None and filename is not None:
        f = open(filepath, "rb")
        obj, created = SupplierReceipt.objects.update_or_create(
            supplier=supplier,
            mode_of_payment=mode_of_payment,
            reference=reference,
            amount=amount,
            payment_date=payment_date,
        )
        print(obj, created)
        if created:
            obj.receipt.save(filename, File(f))
            print(obj)
            f.close()
        else:
            pass
    else:
        pass