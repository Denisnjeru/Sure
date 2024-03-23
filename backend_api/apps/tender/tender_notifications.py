from celery import shared_task
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from sentry_sdk import capture_exception
from backend.storage_backends import PrivateMediaStorage
import datetime
import os
from contextlib import contextmanager
from pathlib import Path
from django.utils.translation import gettext_lazy as _
import numpy as np
import requests
from django import apps
from django.contrib.contenttypes.models import ContentType
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from ..core.utils import write_pdf, default_from_email_sendinblue, connection
from celery import Task
from celery_progress.backend import ProgressRecorder
from .models import Tender


def email_category_notifications(data, files, category_id):

    level = data["level"]
    verb = data["verb"]
    subject = data["subject"]
    message = data["content"]
    potential_selection = data["selection_potential"]
    nonresponsive_selection = data["nonresponsive_selection"]
    type_class = data["to"]
    emailed = True
    model_content_type = "category"
    category = apps.apps.get_model('tender', 'Category').objects.filter(
        id=category_id
    ).prefetch_related('tender').first()
    job = category.tender
    company_id = job.company_id

    if type_class == "all":
        try:
            category_type_suppliers = []
            potential_dictionary = {}
            category_type = category.category_type
            potential_dictionary = category_type.suppliers_list(job.company.country)
            category_type_suppliers.extend(potential_dictionary["registered_suppliers"])
            category_type_suppliers.extend(potential_dictionary["old_suppliers"])
            print(category_type_suppliers)
            if category_type_suppliers:
                suppliers = category_type_suppliers
                for supplier in suppliers:

                    if supplier._meta.model.__name__ == "CategoryTypeSupplier":
                        email = supplier.primary_email
                        if files:
                            # files = request.FILES.getlist("files")
                            send_email_notification(supplier, subject, message, files, True)
                            create_new_email_notification(
                                level, email, category_id, subject, verb, emailed, model_content_type,
                                company_id, type_class, message, files, True
                            )
                        else:
                            send_email_notification(supplier, subject, message, None, True)
                            create_new_email_notification(
                                level, email, category_id, subject, verb, emailed, model_content_type,
                                company_id, type_class, message, None, True,
                            )
                    else:
                        email = supplier.email
                        if files:
                            # files = request.FILES.getlist("files")
                            send_email_notification(supplier, subject, message, files)
                            create_new_email_notification(
                                level, email, category_id, subject, verb, emailed, model_content_type,
                                company_id, type_class, message, files,
                            )
                        else:
                            send_email_notification(supplier, subject, message)
                            create_new_email_notification(
                                level, email, category_id, subject, verb, emailed, model_content_type,
                                company_id, type_class, message,
                            )

            message = 'Email Notifications sent successfully!'
            return
        except Exception as e:
            message = 'Email Notifications were not sent!'
            # capture_exception(e)
            return
    if type_class == "paid":
        try:
            paid_bidders = category.paid_bidders
            print(paid_bidders)
            if paid_bidders:
                for bidder in paid_bidders:
                    email = bidder.email
                    if files:
                        # files = request.FILES.getlist("files")
                        send_email_notification(bidder, subject, message, files)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message, files
                        )
                    else:
                        send_email_notification(bidder, subject, message)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message,
                        )

            message = "Email Notifications sent successfully!"
            return
        except Exception as e:
            message = "Email Notifications were not sent!"
            capture_exception(e)
            print(e)
            context = {
                "response_message": "An error occured",
                "messages": [message, ]
            }
            return context
    if type_class == "potential":
        if potential_selection == "custom":
            category_type = category.category_type
            # calculate potential suppliers
            paid_bidders = category.paid_bidders
            if paid_bidders:
                potential_suppliers = calculate_potential_suppliers(
                    paid_bidders, category
                )
            elif len(paid_bidders) == 0:
                category_type_suppliers = []
                potential_dictionary = {}
                potential_dictionary = category_type.suppliers_list(
                    category.job.company.country
                )
                category_type_suppliers.extend(
                    potential_dictionary["registered_suppliers"]
                )
                category_type_suppliers.extend(
                    potential_dictionary["old_suppliers"]
                )
                potential_suppliers = category_type_suppliers

            try:
                if potential_suppliers:
                    for potential_supplier in potential_suppliers:
                        if potential_supplier._meta.model.__name__ == "CategoryTypeSupplier":
                            email = potential_supplier.primary_email
                            if files:
                                # files = request.FILES.getlist("files")
                                send_email_notification(potential_supplier, subject, message, files, True)
                                create_new_email_notification(
                                    level, email, category_id, subject, verb, emailed, model_content_type,
                                    company_id, type_class, message, files, True,
                                )
                            else:
                                send_email_notification(potential_supplier, subject, message, None, True)
                                create_new_email_notification(
                                    level, email, category_id, subject, verb, emailed, model_content_type,
                                    company_id, type_class, message, None, True
                                )
                        else:
                            email = potential_supplier.email
                            if files:
                                # files = request.FILES.getlist("files")
                                send_email_notification(potential_supplier, subject, message, files)
                                create_new_email_notification(
                                    level, email, category_id, subject, verb, emailed,
                                    model_content_type, company_id, type_class, message, files
                                )
                            else:
                                send_email_notification(potential_supplier, subject, message)
                                create_new_email_notification(
                                    level, email, category_id, subject, verb, emailed,
                                    model_content_type, company_id, type_class, message,
                                )

                message = "Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Email Notifications were not sent!"
                capture_exception(e)
                return
        elif potential_selection == "Default":
            try:
                potential_suppliers_emails = calculate_potential_supplier_default(
                    category.paid_bidders, category
                )
                default_email(potential_suppliers_emails, category)
                # Note  it dosent  create a notification  object
                message = "Default emails sent successfully!"
                return
            except Exception as e:
                message = "Default emails were not sent!"
                capture_exception(e)
                return

        elif potential_selection == "Reminder":
            potential_suppliers_emails = calculate_potential_supplier_default(
                category.paid_bidders, category
            )
            try:
                if potential_suppliers_emails:
                    send_potential_email_remainder_notification(potential_suppliers_emails, category)

                message = "Reminder Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Reminder Email Notifications were not sent!"
                capture_exception(e)
                return
        elif potential_selection == "Extension":
            potential_suppliers_emails = calculate_potential_supplier_default(
                category.paid_bidders, category
            )
            try:
                if potential_suppliers_emails:
                    send_potential_email_extension_notification(potential_suppliers_emails, category)

                message = "Extension Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Extension Email Notifications were not sent!"
                capture_exception(e)
                return
    elif type_class == "qualified":
        if category.status_open:
            message = "Category is still open !"
            return
        else:
            try:
                qualified_bidders = category.qualified_bidders
                for qualified_bidder in qualified_bidders:
                    email = qualified_bidder.email
                    if files:
                        # files = request.FILES.getlist("files")
                        send_email_notification(qualified_bidder, subject, message, files)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message, files,
                        )
                    else:
                        send_email_notification(qualified_bidder, subject, message)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message,
                        )

                message = "Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Email Notifications were not sent!"
                capture_exception(e)
                print(e)
                context = {
                    "response_message": "An error occured",
                    "messages": [message, ]
                }
                return context

    elif type_class == "unqualified":
        if category.status_open:
            message = "Category is still open !"
            return
        else:
            try:
                unqualified_bidders = category.unqualified_bidders
                for unqualified_bidder in unqualified_bidders:
                    email = unqualified_bidder.email

                    if files:
                        # files = request.FILES.getlist("files")
                        send_email_notification(unqualified_bidder, subject, message, files)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message, files,
                        )
                    else:
                        send_email_notification(unqualified_bidder, subject, message)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed, model_content_type,
                            company_id, type_class, message,
                        )

                message = "Email Notifications sent successfully!"
                return

            except Exception as e:
                message = "Email Notifications were not sent!"
                capture_exception(e)
                return
    elif type_class == "responsive":
        try:
            responsive_bidders = category.responsive_bidders
            for responsive_bidder in responsive_bidders:
                email = responsive_bidder.email

                if files:
                    # files = request.FILES.getlist("files")
                    send_email_notification(responsive_bidder, subject, message, files)
                    create_new_email_notification(
                        level, email, category_id, subject, verb, emailed, model_content_type,
                        company_id, type_class, message, files
                    )
                else:
                    send_email_notification(responsive_bidder, subject, message)
                    create_new_email_notification(
                        level, email, category_id, subject, verb, emailed, model_content_type,
                        company_id, type_class, message,
                    )
            message = "Email Notifications sent successfully!"
            return
        except Exception as e:
            message = "Email Notifications were not sent!"
            capture_exception(e)
            return
    elif type_class == "non-responsive":
        try:
            non_responsive_bidders = category.non_responsive_bidders
            if nonresponsive_selection == "Custom":
                for non_responsive_bidder in non_responsive_bidders:
                    email = non_responsive_bidder.email

                    if files:
                        # files = request.FILES.getlist("files")
                        send_email_notification(
                            non_responsive_bidder, subject, message, files
                        )
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed,
                            model_content_type, company_id, type_class, message, files,
                        )
                    else:
                        send_email_notification(
                            non_responsive_bidder, subject, message
                        )
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed,
                            model_content_type, company_id, type_class, message,
                        )
            elif nonresponsive_selection == "Reminder":
                for non_responsive_bidder in non_responsive_bidders:
                    email = non_responsive_bidder.email
                    send_non_responsve_email_remainder_notification(
                        non_responsive_bidder, category
                    )
                    create_new_email_notification(
                        level, email, category_id, subject, verb, emailed,
                        model_content_type, company_id, type_class, message,
                    )

            message = "Email Notifications sent successfully!"
            return
        except Exception as e:
            message = "Email Notifications were not sent!"
            capture_exception(e)
            return
    else:
        try:
            if len(data["specific-bidder"]) > 0:
                for specificbidder in data["specific-bidder"]:
                    bidder = apps.apps.get_model('suppliers', 'Supplier').objects.get(email=specificbidder)
                    email = specificbidder

                    if files:
                        # files = request.FILES.getlist("files")
                        send_email_notification(bidder, subject, message, files)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed,
                            model_content_type, company_id, type_class, message, files,
                        )
                    else:
                        send_email_notification(bidder, subject, message)
                        create_new_email_notification(
                            level, email, category_id, subject, verb, emailed,
                            model_content_type, company_id, type_class, message,
                        )

                message = "Email Notifications sent successfully"
                return
            else:
                message = "No bidder was selected"
                return
        except Exception as e:
            message = "Email Notifications were not sent!"
            capture_exception(e)
            return


def send_email_notification(bidder, subject, text, files=None, old=None):
    try:
        message = render_to_string(
            "tender/emails/supplier/notification.html",
            {"user": bidder, "message": text},
        )

        if old == None:
            to_email = bidder.email
        else:
            to_email = bidder.primary_email

        email = EmailMultiAlternatives(
            subject, message, to=[to_email],
            from_email=default_from_email_sendinblue, connection=connection,
        )
        email.attach_alternative(message, "text/html")
        if files:
            for f in files:
                fl = f.file
                with uncloseable(fl):
                    email.attach(f.name, fl.getvalue(), f.content_type)
        email.send(fail_silently=True)
    except Exception as e:
        capture_exception(e)
        print(e)
        pass


def create_new_email_notification(
        level, email, object_id, subject, verb, emailed, model_content_type,
        company_id, type_class, message, files=None, old=None):
    supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(email=email).first()
    try:
        if old == None:
            new_notification = apps.apps.get_model('core', 'Notification').objects.create(
                level=level, recipient=supplier,
                target_content_type=ContentType.objects.get(app_label="auth", model="user"),
                target_object_id=supplier.id, actor_object_id=company_id,
                actor_content_type=ContentType.objects.get(app_label="qed", model="company"),
                action_object_content_type=ContentType.objects.get(app_label="qed", model=model_content_type),
                action_object_object_id=object_id, emailed=emailed, description=subject, verb=verb,
                data=message, type_class=type_class,
            )
        else:
            new_notification = apps.apps.get_model('core', 'Notification').objects.create(
                level=level,
                target_content_type=ContentType.objects.get(app_label="qed", model="categorytypesupplier"),
                target_object_id=apps.apps.get_model(
                    'core', 'CategoryTypeSupplier').objects.filter(primary_email=email).first().id,
                action_object_content_type=ContentType.objects.get(app_label="qed", model=model_content_type),
                action_object_object_id=object_id, emailed=emailed, description=subject,verb=verb,
                data=message,type_class=type_class,
            )

        if files:
            for f in files:
                with uncloseable(f):
                    doc = apps.apps.get_model('core', 'NotificationDocument').objects.create(
                        name=f.name, document_url=f, notification=new_notification
                    )
                    doc_new = doc
                    doc_new.save()

        return True
    except Exception as e:
        # capture_exception(e)
        return False


def calculate_potential_supplier_default(paid_bidders, category):
    paid_bidders_suppliers = []
    potential = []
    # get paid suppliers  emails
    for supplier in paid_bidders:
        paid_bidders_suppliers.append(supplier.email)

    # get list all  categoryType supplier emails
    category_type_suppliers = category.category_type.suppliers_list(
        country=category.tender.company.country
    )
    category_type_suppliers_suppliers = list(category_type_suppliers["old_suppliers"])
    registered_suppliers = category_type_suppliers["registered_suppliers"]
    category_type_suppliers_suppliers.extend(registered_suppliers)

    potential = list(
        (set(paid_bidders_suppliers) | set(category_type_suppliers_suppliers))
        - (set(category_type_suppliers_suppliers) & set(paid_bidders_suppliers))
    )
    return potential


def send_non_responsve_email_remainder_notification(bidder, category):
    countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
    job = category.tender
    company = job.company
    country = company.country

    try:
        if country not in countries:
            body = render_to_string(
                "tender/emails/supplier/non_responsive_remainder_count.html",
                {
                    "supplier": bidder.company_name, "company": company,
                    "category": category, "Date": category.closing_date.date(),
                    "Time": category.closing_date.time().strftime("%H:%M"),
                },
            )

            message = render_to_string(
                "tender/emails/supplier/non_responsive_remainder_count.html",
                {
                    "supplier": bidder.company_name, "company": company,
                    "category": category, "Date": category.closing_date.date(),
                    "Time": category.closing_date.time().strftime("%H:%M"),
                },
            )
        else:
            # send with  personalized phone and email
            help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
            body = render_to_string(
                "tender/emails/supplier/custom/non_responsive_remainder_count.html",
                {
                    "supplier": bidder.company_name, "company": company,
                    "category": category,"Date": category.closing_date.date(),
                    "Time": category.closing_date.time().strftime("%H:%M"),
                    "phone": help_contacts.contact_phone,
                    "help_email": help_contacts.helpemail,
                },
            )

            message = render_to_string(
                "tender/emails/supplier/custom/non_responsive_remainder_count.html",
                {
                    "supplier": bidder.company_name, "company": company,
                    "category": category, "Date": category.closing_date.date(),
                    "Time": category.closing_date.time().strftime("%H:%M"),
                    "phone": help_contacts.contact_phone,
                    "help_email": help_contacts.helpemail,
                },
            )

        email_subject = f"{job.title.upper()} REMINDER"

        email = EmailMultiAlternatives(
            subject=email_subject, body=body, to=[bidder.email]
        )
        email.attach_alternative(message, "text/html")
        email.send(fail_silently=True)
        return True
    except Exception as e:
        capture_exception(e)
        return False


def send_potential_email_extension_notification(suppliers, category):
    countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
    job = category.tender
    company = job.company
    country = company.country

    if len(suppliers) >= 99:
        half = len(suppliers) // 2
        second_half = suppliers[:half]
        suppliers = suppliers[half:]
        try:
            if country not in countries:
                body = render_to_string(
                    "tender/emails/supplier/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
                body = render_to_string(
                    "tender/emails/supplier/custom/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/custom/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

            email_subject = (
                f"{job.title.upper()} DEADLINE EXTENSION NOTICE"
            )

            A = PrivateMediaStorage()
            headers = {"ResponseContentDisposition": f"attachment;"}
            time = datetime.datetime.now()
            file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
            dir_name = Path(
                "media/temp/{}/{}/{}".format(time.year, time.month, time.day)
            )  # folder structure
            dir_name.mkdir(parents=True, exist_ok=True)
            file_name = os.path.basename(f"{job.advert}")
            filepath = "{}/{}".format(dir_name, file_name)

            r = requests.get(file_url)
            with open("{}".format(filepath), "wb") as f:
                f.write(r.content)

            email = EmailMultiAlternatives(
                subject=email_subject, body=body, bcc=suppliers,
                from_email=default_from_email_sendinblue, connection=connection,
            )
            email.attach_alternative(message, "text/html")
            email.attach_file(filepath)
            email.send(fail_silently=True)
            # print(f"sending second half")
            send_potential_email_extension_notification(second_half, category)
            return True
        except Exception as e:
            capture_exception(e)
            send_potential_email_extension_notification(second_half, category)
            return False
    else:
        try:
            if country not in countries:
                body = render_to_string(
                    "tender/emails/supplier/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
                body = render_to_string(
                    "tender/emails/supplier/custom/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/custom/potential_extension.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

            email_subject = (
                f"{job.title.upper()} DEADLINE EXTENSION NOTICE"
            )

            A = PrivateMediaStorage()
            headers = {"ResponseContentDisposition": f"attachment;"}
            time = datetime.datetime.now()
            file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
            dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
            dir_name.mkdir(parents=True, exist_ok=True)
            file_name = os.path.basename(f"{job.advert}")
            filepath = "{}/{}".format(dir_name, file_name)

            r = requests.get(file_url)
            with open("{}".format(filepath), "wb") as f:
                f.write(r.content)

            email = EmailMultiAlternatives(
                subject=email_subject, body=body, bcc=suppliers,
                from_email=default_from_email_sendinblue, connection=connection,
            )
            email.attach_alternative(message, "text/html")
            email.attach_file(filepath)
            email.send(fail_silently=True)
            return True
        except Exception as e:
            capture_exception(e)
            return False


def send_potential_email_remainder_notification(suppliers, category):
    countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
    job = category.tender
    company = job.company
    country = company.country

    if len(suppliers) >= 99:
        no_of_suppliers = len(suppliers)
        no_of_lists = no_of_suppliers // 99
        if no_of_suppliers % 99 != 0:
            no_of_lists += 1
        split_suppliers = np.array_split(suppliers, no_of_lists)
        # print(f"list  with  lists {split_suppliers}")
        count = 1
        for split_supplier in split_suppliers:
            split_supplier = list(split_supplier)
            # print(f"list number: {count} this  is the list: {split_supplier}")
            try:
                if country not in countries:
                    body = render_to_string(
                        "tender/emails/supplier/potential_remainder_count.html",
                        {
                            "supplier": "Esteemed Vendor", "company": company,
                            "category": category.name, "Date": category.closing_date.date(),
                            "Time": category.closing_date.time().strftime("%H:%M"),
                        },
                    )

                    message = render_to_string(
                        "tender/emails/supplier/potential_remainder_count.html",
                        {
                            "supplier": "Esteemed Vendor", "company": company,
                            "category": category.name, "Date": category.closing_date.date(),
                            "Time": category.closing_date.time().strftime("%H:%M"),
                        },
                    )
                else:
                    # send with  personalized phone and email
                    help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
                    body = render_to_string(
                        "tender/emails/supplier/custom/potential_remainder_count.html",
                        {
                            "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                            "Date": category.closing_date.date(),
                            "Time": category.closing_date.time().strftime("%H:%M"),
                            "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                        },
                    )

                    message = render_to_string(
                        "supplier_portal/emails/custom_emails/potential_remainder_count.html",
                        {
                            "supplier": "Esteemed Vendor", "company": company,
                            "category": category.name, "Date": category.closing_date.date(),
                            "Time": category.closing_date.time().strftime("%H:%M"),
                            "phone": help_contacts.contact_phone,
                            "help_email": help_contacts.helpemail,
                        },
                    )

                email_subject = f"{job.title.upper()} REMINDER"

                A = PrivateMediaStorage()
                headers = {"ResponseContentDisposition": f"attachment;"}
                time = datetime.datetime.now()
                file_url = A.url(f"{category.job.advert}", expire=300, parameters=headers,
                                 http_method="GET")
                dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                dir_name.mkdir(parents=True, exist_ok=True)
                file_name = os.path.basename(f"{job.advert}")
                filepath = "{}/{}".format(dir_name, file_name)

                r = requests.get(file_url)
                with open("{}".format(filepath), "wb") as f:
                    f.write(r.content)

                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, bcc=split_supplier,
                    from_email=default_from_email_sendinblue, connection=connection,
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(filepath)
                email.send(fail_silently=True)
            except Exception as e:
                capture_exception(e)
            count += 1
        return True
    else:
        try:
            if country not in countries:
                body = render_to_string(
                    "tender/emails/supplier/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model('core', 'HelpContact').objects.get(country=country)
                body = render_to_string(
                    "tender/emails/supplier/custom/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/custom/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company,
                        "category": category.name, "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

            email_subject = f"{job.title.upper()} REMINDER"

            A = PrivateMediaStorage()
            headers = {"ResponseContentDisposition": f"attachment;"}
            time = datetime.datetime.now()
            file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
            dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
            dir_name.mkdir(parents=True, exist_ok=True)
            file_name = os.path.basename(f"{job.advert}")

            filepath = "{}/{}".format(dir_name, file_name)
            r = requests.get(file_url)
            with open("{}".format(filepath), "wb") as f:
                f.write(r.content)

            email = EmailMultiAlternatives(
                subject=email_subject, body=body, bcc=suppliers,
                from_email=default_from_email_sendinblue, connection=connection,
            )
            email.attach_alternative(message, "text/html")
            email.attach_file(filepath)
            email.send(fail_silently=True)
            return True
        except Exception as e:
            print(f"Exception is {e}")
            capture_exception(e)
            return False


def default_email(potential_suppliers_emails, category):
    countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
    job = category.tender
    company = job.company
    country = company.country
    if len(potential_suppliers_emails) >= 99:
        half = len(potential_suppliers_emails) // 2
        second_half = potential_suppliers_emails[:half]
        potential_suppliers_emails = potential_suppliers_emails[half:]
        try:
            if country not in countries:
                body = render_to_string(
                    "tender/emails/supplier/supplier_invite.html",
                    {"supplier": "Esteemed Vendor", "company": company,
                     "category": category.name},
                )

                message = render_to_string(
                    "tender/emails/supplier/supplier_invite.html",
                    {"supplier": "Esteemed Vendor", "company": company,
                     "category": category.name},
                )

                email_subject = f"{job.title.upper()} NOTICE"

                A = PrivateMediaStorage()
                headers = {"ResponseContentDisposition": f"attachment;"}
                time = datetime.datetime.now()
                file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
                dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                dir_name.mkdir(parents=True, exist_ok=True)
                file_name = os.path.basename(f"{job.advert}")
                filepath = "{}/{}".format(dir_name, file_name)

                r = requests.get(file_url)
                with open("{}".format(filepath), "wb") as f:
                    f.write(r.content)

                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, bcc=potential_suppliers_emails,
                    from_email=default_from_email_sendinblue, connection=connection,
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(filepath)
                email.send(fail_silently=True)
                default_email(second_half, category)
                return True
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
                body = render_to_string(
                    "tender/emails/supplier/custom/supplier_invite.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/custom/supplier_invite.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                email_subject = f"{job.title.upper()} NOTICE"

                A = PrivateMediaStorage()
                headers = {"ResponseContentDisposition": f"attachment;"}
                time = datetime.datetime.now()
                file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
                dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                dir_name.mkdir(parents=True, exist_ok=True)
                file_name = os.path.basename(f"{job.advert}")
                filepath = "{}/{}".format(dir_name, file_name)

                r = requests.get(file_url)
                with open("{}".format(filepath), "wb") as f:
                    f.write(r.content)

                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, bcc=potential_suppliers_emails,
                    from_email=default_from_email_sendinblue, connection=connection,
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(filepath)
                email.send(fail_silently=True)
                default_email(second_half, category)
                return True
        except Exception as e:
            capture_exception(e)
            default_email(second_half, category)
            return False
    else:
        try:
            if country not in countries:
                body = render_to_string(
                    "tender/emails/supplier/supplier_invite.html",
                    {"supplier": "Esteemed Vendor", "company": company, "category": category.name},
                )

                message = render_to_string(
                    "tender/emails/supplier/supplier_invite.html",
                    {"supplier": "Esteemed Vendor", "company": company, "category": category.name},
                )

                email_subject = f"{job.title.upper()} NOTICE"

                A = PrivateMediaStorage()
                headers = {"ResponseContentDisposition": f"attachment;"}
                time = datetime.datetime.now()
                file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
                dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                dir_name.mkdir(parents=True, exist_ok=True)
                file_name = os.path.basename(f"{job.advert}")
                filepath = "{}/{}".format(dir_name, file_name)

                r = requests.get(file_url)
                with open("{}".format(filepath), "wb") as f:
                    f.write(r.content)

                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, bcc=potential_suppliers_emails,
                    from_email=default_from_email_sendinblue, connection=connection,
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(filepath)
                email.send(fail_silently=True)
                return True
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model('core', 'Helpcontacts').objects.get(country=country)
                body = render_to_string(
                    "tender/emails/supplier/custom/supplier_invite.html",
                    {
                        "supplier": "Esteemed Vendor", "company": company, "category": category.name,
                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "tender/emails/supplier/custom/supplier_invite.html",
                    {
                        "supplier": "Esteemed Vendor", "company": category.job.company,
                        "category": category.name,"phone": help_contacts.contact_phone,
                        "help_email": help_contacts.helpemail,
                    },
                )

                email_subject = f"{job.title.upper()} NOTICE"

                A = PrivateMediaStorage()
                headers = {"ResponseContentDisposition": f"attachment;"}
                time = datetime.datetime.now()
                file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
                dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                dir_name.mkdir(parents=True, exist_ok=True)
                file_name = os.path.basename(f"{job.advert}")
                filepath = "{}/{}".format(dir_name, file_name)

                r = requests.get(file_url)
                with open("{}".format(filepath), "wb") as f:
                    f.write(r.content)

                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, bcc=potential_suppliers_emails,
                    from_email=default_from_email_sendinblue, connection=connection,
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(filepath)
                email.send(fail_silently=True)
                return True
        except Exception as e:
            capture_exception(e)
            return False


def calculate_potential_suppliers(paid_bidders, category):
    paid_bidders_suppliers = []
    # category_type_suppliers_suppliers = []
    potential = []

    for supplier in paid_bidders:
        paid_bidders_suppliers.append(supplier.email)

    # get list all  categoryType supplier emails
    category_type_suppliers = category.category_type.suppliers_list(
        country=category.tender.company.country
    )
    category_type_suppliers_suppliers = list(category_type_suppliers["old_suppliers"])
    registered_suppliers = category_type_suppliers["registered_suppliers"]
    category_type_suppliers_suppliers.extend(registered_suppliers)

    potential_supplier_email = list(
        (set(paid_bidders_suppliers) | set(category_type_suppliers_suppliers))
        - (set(category_type_suppliers_suppliers) & set(paid_bidders_suppliers))
    )

    for supplier_email in potential_supplier_email:
        supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(email=supplier_email).first()
        if supplier:
            potential.append(supplier)
        else:
            potential.append(
                apps.apps.get_model('core', 'CategoryTypeSupplier').objects.filter(
                    primary_email=supplier_email
                ).first()
            )

    print(potential)
    return potential


@contextmanager
def uncloseable(fd):
    """
    Context manager which turns the fd's close operation to no-op for the duration of the context.
    """
    close = fd.close
    fd.close = lambda: None
    yield fd
    fd.close = close


@shared_task()
def initiate_email_out_sending(job_id):
    job = apps.apps.get_model("tender", "Tender").objects.get(id=job_id)
    categories = job.categories

    A = PrivateMediaStorage()
    headers = {"ResponseContentDisposition": f"attachment;"}
    time = datetime.datetime.now()
    file_url = A.url(f"{job.advert}", expire=300, parameters=headers, http_method="GET")
    dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))  # folder structure
    dir_name.mkdir(parents=True, exist_ok=True)
    file_name = os.path.basename(f"{job.advert}")
    filepath = "{}/{}".format(dir_name, file_name)
    r = requests.get(file_url)
    with open("{}".format(filepath), "wb") as f:
        f.write(r.content)

    for category in categories:
        date = datetime.datetime.now()
        emails = apps.apps.get_model("tender", "EmailOut").objects.filter(
            category_id=category.id, sent=False, type=apps.apps.get_model("tender", "EmailOut").REMINDER, has_error=False,
            created_at__year=date.year, created_at__month=date.month, created_at__day=date.day, 
            target__model="tender"
        ).order_by('-id')
        c = emails.count()

        while c > 0:
            to_send = apps.apps.get_model("tender", "EmailOut").objects.filter(
                category_id=category.id, sent=False, type=apps.apps.get_model("tender", "EmailOut").REMINDER, has_error=False,
                created_at__year=date.year, created_at__month=date.month, created_at__day=date.day,
                target__model="tender"
            ).order_by('-id')[:90]
            instance = to_send.first()

            ids = []
            send_to = []
            for i in to_send:
                send_to.append(i.to.replace(" ", ""))
                ids.append(i.id)
            try:
                email = EmailMultiAlternatives(
                    subject=instance.subject, body=instance.body,
                    bcc=send_to, from_email=default_from_email_sendinblue,
                    connection=connection,
                )
                email.attach_alternative(instance.message, "text/html")
                email.attach_file(filepath)

                email.send()
                apps.apps.get_model("tender", "EmailOut").objects.filter(id__in=ids).update(sent=True)
            except Exception as e:
                capture_exception(e)
                apps.apps.get_model("tender", "EmailOut").objects.filter(id__in=ids).update(error=f"{e}", has_error=True)
            c -= 90
    return


class SendTenderEmailNotifications(Task):
    name = "SendTenderEmailNotifications"
    progress_recorder = None
    result = 0

    def run(self, *args, **kwargs):
        self.progress_recorder = ProgressRecorder(self)
        type_class = kwargs["data"]["type"]

        if type_class == "potential":
            potential_selection = kwargs["data"]["potential_selection"]
            if potential_selection == "Default":
                context = self.send_potential_default(kwargs["job_id"], kwargs["data"])
                return context
            elif potential_selection == "Extension":
                context = self.send_potential_extension(kwargs["job_id"], kwargs["data"])
                return context
            elif potential_selection == "Reminder":
                context = self.send_potential_reminder(kwargs["job_id"], kwargs["data"])
                return context
        elif type_class == "non-responsive":
            non_responsive_selection = kwargs["data"]["non_responsive_selection"]
            if non_responsive_selection == "Reminder":
                context = self.send_non_responsive_email_remainder_notification(kwargs["job_id"], kwargs["data"])
                return context
        return

    def send_potential_reminder(self, job_id, data):
        messages = []
        job = apps.apps.get_model("tender", "Tender").objects.get(id=job_id)
        categories = job.categories

        for category in categories:
            potential_suppliers_emails = calculate_potential_supplier_default(
                category.paid_bidders, category
            )
            try:
                if potential_suppliers_emails:
                    self.store_potential_email_remainder_notification(potential_suppliers_emails, category)
            except Exception as e:
                messages.append(f"Reminder Email Notifications for {category.name} were not sent!",)
                capture_exception(e)

        initiate_email_out_sending.delay(job_id=job_id)
        context = {
            "response_message": "Reminder Email Notifications for all categories sent successfully!",
            "messages": messages
        }
        return context

    def send_potential_extension(self, job_id, data):
        job = apps.apps.get_model("tender", "Tender").objects.get(id=job_id)
        categories = job.categories
        messages = []

        for category in categories:
            potential_suppliers_emails = calculate_potential_supplier_default(
                category.paid_bidders, category
            )
            try:
                if potential_suppliers_emails:
                    send_potential_email_extension_notification(
                        potential_suppliers_emails, category
                    )
            except Exception as e:
                messages.append(f"Extension Email Notifications for {category.name} were not sent!",)
                capture_exception(e)

        context = {
            "response_message": "Extension Email Notifications for all categories sent successfully!",
            "messages": messages
        }
        return context

    def send_potential_default(self, job_id, data):
        job = apps.apps.get_model("tender", "Tender").objects.get(id=job_id)
        categories = job.categories
        messages = []

        for category in categories:
            potential_suppliers_emails = calculate_potential_supplier_default(
                category.paid_bidders, category
            )
            try:
                if potential_suppliers_emails:
                    default_email(potential_suppliers_emails, category)
            except Exception as e:
                messages.append(f"Reminder Email Notifications for {category.name} were not sent!")
                capture_exception(e)

        context = {
            "response_message": "Default Email Notifications for all categories sent successfully!",
            "messages": messages
        }
        return context

    def store_potential_email_remainder_notification(self, suppliers, category):
        countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
        country = category.job.company.country
        job = category.job
        company = job.company

        try:
            if country not in countries:
                body = render_to_string(
                    "supplier_portal/emails/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": company,
                        "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )

                message = render_to_string(
                    "supplier_portal/emails/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": company,
                        "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                    },
                )
            else:
                # send with  personalized phone and email
                help_contacts = apps.apps.get_model("core", "HelpContact").objects.get(country=country)
                body = render_to_string(
                    "supplier_portal/emails/custom_emails/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": company,
                        "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone,
                        "help_email": help_contacts.helpemail,
                    },
                )

                message = render_to_string(
                    "supplier_portal/emails/custom_emails/potential_remainder_count.html",
                    {
                        "supplier": "Esteemed Vendor",
                        "company": company,
                        "category": category.name,
                        "Date": category.closing_date.date(),
                        "Time": category.closing_date.time().strftime("%H:%M"),
                        "phone": help_contacts.contact_phone,
                        "help_email": help_contacts.helpemail,
                    },
                )

            email_subject = f"{job.job_title.upper()} REMINDER"
            emails_to_store = []
            for supplier in suppliers:
                if supplier != "" and supplier != " " and supplier is not None:
                    try:
                        emails_to_store.append(
                            apps.apps.get_model("tender", "EmailOut")(
                                subject=email_subject,
                                to=supplier, message=message, body=body, category_id=category.id,
                                type=apps.apps.get_model("tender", "EmailOut").REMINDER,
                                target__model="tender"
                            )
                        )
                        if len(emails_to_store) >= 90:
                            apps.apps.get_model("tender", "EmailOut").objects.bulk_create(emails_to_store)
                            emails_to_store.clear()
                    except Exception as e:
                        emails_to_store.clear()
                        capture_exception(e)
                        pass
            apps.apps.get_model("tender", "EmailOut").objects.bulk_create(emails_to_store)
            emails_to_store.clear()
            return True
        except Exception as e:
            capture_exception(e)
            return True

    def send_non_responsive_email_remainder_notification(self, job_id, data):
        job = apps.apps.get_model("tender", "Tender").objects.get(id=job_id)
        countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
        country = job.company.country

        categories = job.categories
        for category in categories:
            bidders = category.non_responsive_bidders_list
            for bidder in bidders:
                try:
                    if country not in countries:
                        body = render_to_string(
                            "supplier_portal/emails/non_responsive_remainder_count.html",
                            {
                                "supplier": bidder.company_name,
                                "company": category.job.company,
                                "category": category,
                                "Date": category.closing_date.date(),
                                "Time": category.closing_date.time().strftime("%H:%M"),
                            },
                        )

                        message = render_to_string(
                            "supplier_portal/emails/non_responsive_remainder_count.html",
                            {
                                "supplier": bidder.company_name,
                                "company": category.job.company,
                                "category": category,
                                "Date": category.closing_date.date(),
                                "Time": category.closing_date.time().strftime("%H:%M"),
                            },
                        )
                    else:
                        # send with  personalized phone and email
                        help_contacts = apps.apps.get_model("core", "HelpContact").objects.get(country=country)
                        body = render_to_string(
                            "supplier_portal/emails/custom_emails/non_responsive_remainder_count.html",
                            {
                                "supplier": bidder.company_name,
                                "company": category.job.company,
                                "category": category,
                                "Date": category.closing_date.date(),
                                "Time": category.closing_date.time().strftime("%H:%M"),
                                "phone": help_contacts.contact_phone,
                                "help_email": help_contacts.helpemail,
                            },
                        )

                        message = render_to_string(
                            "supplier_portal/emails/custom_emails/non_responsive_remainder_count.html",
                            {
                                "supplier": bidder.company_name,
                                "company": category.job.company,
                                "category": category,
                                "Date": category.closing_date.date(),
                                "Time": category.closing_date.time().strftime("%H:%M"),
                                "phone": help_contacts.contact_phone,
                                "help_email": help_contacts.helpemail,
                            },
                        )

                    email_subject = f"{job.job_title.upper()} REMINDER"

                    email = EmailMultiAlternatives(
                        subject=email_subject, body=body, to=[bidder.email]
                    )
                    email.attach_alternative(message, "text/html")
                    email.send(fail_silently=True)
                except Exception as e:
                    capture_exception(e)
        context = {
            "response_message": "Non responsive bidder reminders sent"
        }
        return context


@shared_task()
def send_tender_job_invite_email(job_id):
    try:
        job = Tender.objects.get(id=job_id)
        for category in job.categories:
            countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
            if category.invite_notification == False:
                if category.invite_only == True:
                    """
                    Send notifications for closed tender
                    """
                    pass
        
                else:
                    """
                    Send notifications for open tender
                    """
                    suppliers = category.category_type.suppliers_list(
                        country=category.job.company.country
                    )
                    tender = category.tender
                    company = tender.company
                    buyer = apps.apps.get_model("buyer", "Buyer").objects.filter(company=company).first()
                    country = tender.company.country
                    old_suppliers = list(suppliers["old_suppliers"])
                    registered_suppliers = suppliers["registered_suppliers"]
                    supplier_emails = old_suppliers.extend(registered_suppliers)
                    # for loop  was here
                    if len(old_suppliers) >= 99:
                        no_of_suppliers = len(old_suppliers)
                        no_of_lists = no_of_suppliers // 99
                        if no_of_suppliers % 99 != 0:
                            no_of_lists += 1
                        split_old_suppliers = np.array_split(old_suppliers, no_of_lists)
        
                        count = 1
                        for split_old_supplier in split_old_suppliers:
                            split_old_supplier = list(split_old_supplier)
                            if country not in countries:
                                try:
                                    body = render_to_string(
                                        "supplier_portal/emails/supplier_invite.html",
                                        {"supplier": "Esteemed Vendor", "company": company, "category": category.name,},)
        
                                    message = render_to_string(
                                        "supplier_portal/emails/supplier_invite.html",
                                        {"supplier": "Esteemed Vendor", "company": company, "category": category.name,},)
                                    email_subject = f"{tender.title.upper()} NOTICE"
        
                                    A = PrivateMediaStorage()
                                    headers = {"ResponseContentDisposition": f"attachment;"}
                                    time = datetime.datetime.now()
                                    file_url = A.url(
                                        f"{tender.advert}", expire=300, parameters=headers, http_method="GET",)

                                    dir_name = Path(
                                        "media/temp/{}/{}/{}".format(time.year, time.month, time.day)) 
                                    dir_name.mkdir(parents=True, exist_ok=True)
                                    file_name = os.path.basename(f"{tender.advert}")
                                    filepath = "{}/{}".format(dir_name, file_name)
                                    r = requests.get(file_url)
                                    with open("{}".format(filepath), "wb") as f:
                                        f.write(r.content)
        
                                    email = EmailMultiAlternatives(
                                        subject=email_subject, body=body, from_email=default_from_email_sendinblue,
                                        bcc=split_old_supplier, connection=connection,)
                                    email.attach_alternative(message, "text/html")
                                    email.attach_file(filepath)
                                    email.send(fail_silently=True)
                                    
                                    Supplier = apps.apps.get_model("suppliers", "Supplier")
                                    try:
                                        for supplier_email in split_old_supplier:
                                            if Supplier.objects.filter(email=supplier_email).exists():
                                                if Supplier.objects.filter(email=supplier_email).exists():
                                                    if supplier_email is not None:
                                                        supplier = Supplier.objects.filter(email=supplier_email).first()
                                                
                                                    buyer = apps.apps.get_model('buyer', 'Buyer').objects.filter(id=buyer.id).first()

                                                    obj, created = apps.apps.get_model("tender", "SupplierBuyerNotification").objects.update_or_create(
                                                        supplier=supplier, buyer=buyer, job=tender, email_subject=email_subject,
                                                        email_body=body, date_sent=datetime.datetime.now(),
                                                    )
                                    except Exception as e:
                                        capture_exception(e)
                                except Exception as e:
                                    capture_exception(e)
        
                                category.invite_notification = True
                                category.save()
                                count += 1
                            else:
                                # send with  personalized phone and email
                                help_contacts = apps.apps.get_model("core","HelpContact").objects.get(country=country)
                                try:
                                    body = render_to_string(
                                        "supplier_portal/emails/custom_emails/supplier_invite.html",
                                        { "supplier": "Esteemed Vendor", "company": company,"category": category.name,
                                            "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,},)
        
                                    message = render_to_string(
                                        "supplier_portal/emails/custom_emails/supplier_invite.html",
                                        {"supplier": "Esteemed Vendor", "company": company, "category": category.name,
                                            "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,
                                        },
                                    )
                                    email_subject = f"{tender.title.upper()} NOTICE"
        
                                    A = PrivateMediaStorage()
                                    headers = {"ResponseContentDisposition": f"attachment;"}
                                    time = datetime.datetime.now()
                                    file_url = A.url(
                                        f"{tender.advert}", expire=300, parameters=headers, http_method="GET",)
                                    dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                                    dir_name.mkdir(parents=True, exist_ok=True)
                                    file_name = os.path.basename(f"{tender.advert}")
                                    filepath = "{}/{}".format(dir_name, file_name)
                                    r = requests.get(file_url)
                                    with open("{}".format(filepath), "wb") as f:
                                        f.write(r.content)
        
                                    email = EmailMultiAlternatives(
                                        subject=email_subject, body=body, bcc=split_old_supplier,
                                        from_email=default_from_email_sendinblue, connection=connection,)
                                    email.attach_alternative(message, "text/html")
                                    email.attach_file(filepath)
                                    email.send(fail_silently=True)
                                except Exception as e:
                                    capture_exception(e)
                                category.invite_notification = True
                                category.save()
                        return True
                    else:
                        if country not in countries:
                            try:
                                body = render_to_string(
                                    "supplier_portal/emails/supplier_invite.html",
                                    {"supplier": "Esteemed Vendor", "company": company,
                                        "category": category.name,},)
        
                                message = render_to_string(
                                    "supplier_portal/emails/supplier_invite.html",
                                    {"supplier": "Esteemed Vendor", "company": company,
                                        "category": category.name,},)
                                email_subject = f"{tender.title.upper()} NOTICE"
        
                                A = PrivateMediaStorage()
                                headers = {"ResponseContentDisposition": f"attachment;"}
                                time = datetime.datetime.now()
                                file_url = A.url(
                                    f"{tender.advert}", expire=300, parameters=headers, http_method="GET",)
                                dir_name = Path(
                                    "media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                                dir_name.mkdir(parents=True, exist_ok=True)
                                file_name = os.path.basename(f"{tender.advert}")
                                filepath = "{}/{}".format(dir_name, file_name)
                                r = requests.get(file_url)
                                with open("{}".format(filepath), "wb") as f:
                                    f.write(r.content)
        
                                email = EmailMultiAlternatives(
                                    subject=email_subject, body=body, from_email=default_from_email_sendinblue, 
                                    bcc=old_suppliers, connection=connection,)
        
                                email.attach_alternative(message, "text/html")
                                email.attach_file(filepath)
                                email.send(fail_silently=True)
                                connection.close()
                            except Exception as e:
                                capture_exception(e)
        
                            category.invite_notification = True
                            category.save()
                            return old_suppliers
                        else:
                            # send with  personalized phone and email
                            help_contacts = apps.apps.get_model("core", "HelpContact").objects.get(country=country)
                            try:
                                body = render_to_string(
                                    "supplier_portal/emails/custom_emails/supplier_invite.html",
                                    {"supplier": "Esteemed Vendor", "company": company,
                                        "category": category.name, "phone": help_contacts.contact_phone,
                                        "help_email": help_contacts.helpemail,},)
        
                                message = render_to_string(
                                    "supplier_portal/emails/custom_emails/supplier_invite.html",
                                    {"supplier": "Esteemed Vendor", "company": company, "category": category.name,
                                        "phone": help_contacts.contact_phone, "help_email": help_contacts.helpemail,},)
                                email_subject = f"{tender.title.upper()} NOTICE"
        
                                A = PrivateMediaStorage()
                                headers = {"ResponseContentDisposition": f"attachment;"}
                                time = datetime.datetime.now()
                                file_url = A.url(
                                    f"{tender.advert}", expire=300, parameters=headers, http_method="GET",)
                                dir_name = Path(
                                    "media/temp/{}/{}/{}".format(time.year, time.month, time.day))
                                dir_name.mkdir(parents=True, exist_ok=True)
                                file_name = os.path.basename(f"{tender.advert}")
                                filepath = "{}/{}".format(dir_name, file_name)
                                r = requests.get(file_url)
                                with open("{}".format(filepath), "wb") as f:
                                    f.write(r.content)
        
                                email = EmailMultiAlternatives(
                                    subject=email_subject, body=body, bcc=old_suppliers,
                                    from_email=default_from_email_sendinblue, connection=connection,)
                                email.attach_alternative(message, "text/html")
                                email.attach_file(filepath)
                                email.send(fail_silently=True)
                                connection.close()
                            except Exception as e:
                                capture_exception(e)
        
                            category.invite_notification = True
                            category.save()
                            return old_suppliers
            else:
                pass
        return
    except Exception as e:
        capture_exception(e)
        return


@shared_task()
def send_tender_job_invite_sms(job_id):
    countries = ["Uganda", "Malawi", "Zambia", "Mozambique"]
    job = Tender.objects.get(id=job_id)
    country = job.company.country
    for category in job.categories:
    
        if category.invite_notification == False:
            count = 0
            suppliers = category.category_type.suppliers_list(
                country=country
            )
            old_suppliers = suppliers["old_suppliers"]
            registered_suppliers = suppliers["registered_suppliers"]

            for registered_supplier in registered_suppliers:
                if registered_supplier.phone_number != "":
                    if country not in countries:
                        category.invite_suppliers_sms(
                            registered_supplier.phone_number, count
                        )
                        count += 1
                    else:
                        category.invite_suppliers_sms(
                            registered_supplier.phone_number, count, country
                        )
                        count += 1
                else:
                    continue

            # for old suppliers
            for old_supplier in old_suppliers:
                if old_supplier.primary_phone != "":
                    if country not in countries:
                        category.invite_suppliers_sms(old_supplier.primary_phone, count)
                        count += 1
                    else:
                        category.invite_suppliers_sms(
                            old_supplier.primary_phone, count, country
                        )
                        count += 1
                else:
                    continue

            category.invite_notification = True
            category.save()
            return suppliers
    return False


# job
def email_job_notifications(request, job_id):
    if request.method == "POST":
        level = request.POST["level"]
        verb = request.POST["verb"]
        subject = request.POST["subject"]
        message = request.POST["content"]
        potential_selection = request.POST["selection_potential"]
        type_class = request.POST["to"]
        emailed = True
        model_content_type = "job"
        job = apps.apps.get_model('tender', 'Tender').objects.get(id=job_id)
        company_id = job.company_id
        categories = job.categories

        if type_class == "all":
            try:
                suppliers = job.participants
                for cat_supplier in suppliers:
                    for supplier in cat_supplier:
                        email = supplier.email
                        print(email)

                        if request.FILES.getlist("files"):
                            files = request.FILES.getlist("files")
                            send_email_notification(supplier, subject, message, files)

                        else:
                            send_email_notification(supplier, subject, message)

                message = "Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Email Notifications were not sent!"
                capture_exception(e)
                return
        if type_class == "paid":
            try:
                for category in categories:
                    if category.paid_bidders:
                        paid_bidders = category.paid_bidders
                        for bidder in paid_bidders:
                            email = bidder.email
                            if request.FILES.getlist("files"):
                                files = request.FILES.getlist("files")
                                send_email_notification(bidder, subject, message, files)
                                create_new_email_notification(
                                    level,
                                    email,
                                    job_id,
                                    subject,
                                    verb,
                                    emailed,
                                    model_content_type,
                                    company_id,
                                    type_class,
                                    message,
                                    files,
                                )
                            else:
                                send_email_notification(bidder, subject, message)
                                create_new_email_notification(
                                    level,
                                    email,
                                    job_id,
                                    subject,
                                    verb,
                                    emailed,
                                    model_content_type,
                                    company_id,
                                    type_class,
                                    message,
                                )

                message = "Email Notifications sent successfully!"
                return
            except Exception as e:
                message = "Email Notifications were not sent!"
                # print(f"{e}")
                # capture_exception(e)
                return


@shared_task()
def send_participants_email(category_id):
    """
    TO be invoked at close of category to send list of participants to the suppliers
    :return:
    """
    try:
        time = datetime.datetime.now()
        category = apps.apps.get_model('tender', 'Category').objects.filter(
            id=category_id
        ).prefetch_related('tender').first()
        job = category.tender
        company = job.company

        participants = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
                question__section__category_id=category_id).only('supplier_id').values('supplier_id').distinct()
        )

        eprocure_email = "tendersure@qedsolutions.co.ke"

        time = datetime.datetime.now()
        file_path = "media/%s/%s/%s/attachments/" % (
            job.company.company_name, job.unique_reference, category.unique_reference,
        )
        filename = "%s_%d_%d.pdf" % (
            category.unique_reference.replace(" ", "_"), time.year, time.month,
        )

        # folder structure
        Path(file_path).mkdir(parents=True, exist_ok=True)
        template_path = "tender/emails/supplier/list_of_participants.html"
        context = {
            "category": category, "participants": participants,
            "job": job, "company": company
        }

        pdf_file_path = write_pdf(
            template_src=template_path,
            context_dict=context,
            file_name=filename,
            file_path=file_path,
        )

        # for each participant, send it
        email_subject = _(
            f"Confirmation of Participation in {job.title} Pre-qualification Exercise"
        )
        invalid_email_suppliers = []

        for participant in participants:
            # check for email address
            try:
                validate_email(participant.email_address)
            except ValidationError as e:
                invalid_email_suppliers.append(participant)
                capture_exception(e)
                continue
            else:
                body = render_to_string(
                    "tender/emails/supplier/list_of_participants_body.html",
                    {
                        "category": category, "participant": participant, "job": job,
                        "company": company
                     },
                )

                message = render_to_string(
                    "tender/emails/supplier/list_of_participants_body.html",
                    {"category": category, "participant": participant},
                )
                email = EmailMultiAlternatives(
                    subject=email_subject, body=body, to=[participant.email_address]
                )
                email.attach_alternative(message, "text/html")
                email.attach_file(pdf_file_path)
                email.send()

        # send one to eprocure as copy
        mail_context = {
            "category": category,
            "eprocure": "Tendersure Team",
        }
        if len(invalid_email_suppliers) > 0:
            mail_context["invalid_email_suppliers"] = invalid_email_suppliers

        body = render_to_string(
            "tender/emails/supplier/list_of_participants_body.html", mail_context
        )

        message = render_to_string(
            "tender/emails/supplier/list_of_participants_body.html",
            {
                "category": category, "eprocure": "Tendersure Team", "job": job,
                "company": company
             },
        )
        email = EmailMultiAlternatives(
            subject=email_subject, body=body, to=[eprocure_email]
        )
        email.attach_alternative(message, "text/html")
        email.attach_file(pdf_file_path)
        email.send()
        context = {
            "response_message": "Notifications sent successfully"
        }
        return context
    except Exception as e:
        context = {
            "response_message": "Error sending emails"
        }
        capture_exception(e)
        return context


@shared_task(bind=True)
def broadcast_tender_job_notifications(self, data):

    job = apps.apps.get_model('tender', 'Tender').objects.get(id=data["job_id"])
    level = data["level"]
    verb = data["verb"]
    description = data["description"]
    type_class = data["type_class"]

    for category in job.categories:
        for bidder in category.paid_bidders:
            new_notification = apps.apps.get_model("core", "Notifications").objects.create(
                level=level,
                recipient=apps.apps.get_model("suppliers", "Supplier").objects.filter(
                    email=bidder.email).first(),
                target_content_type=ContentType.objects.get(
                    app_label="auth", model="user"
                ),
                target_object_id=apps.apps.get_model("suppliers", "Supplier").objects.filter(
                    email=bidder.email)
                .first()
                .id,
                actor_content_type=ContentType.objects.get(
                    app_label="buyer", model="company"
                ),
                actor_object_id=job.company_id,
                action_object_content_type=ContentType.objects.get(
                    app_label="tender", model="category"
                ),
                action_object_object_id=data["job_id"],
                description=description,
                verb=verb,
                type_class=type_class,
            )
    context = {
        "response_message": "Notification sent successfully!"
    }
    return context