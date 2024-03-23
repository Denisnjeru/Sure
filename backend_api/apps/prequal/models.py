import datetime
import math
import re
from pathlib import Path
import os
import pgcrypto
import requests
from django import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SlugField, Avg, Sum
from django.template.defaultfilters import slugify
from django.utils import timezone
from sentry_sdk import capture_exception
from django.template.loader import render_to_string
from apps.core.models import BaseModel, CategoryType, Currency
from apps.core.utils import get_document_url
from django.core.validators import FileExtensionValidator
import numpy as np
from apps.prequal.utils import supplier_response_files, supplier_letters
from apps.suppliers.models import Supplier
from backend.storage_backends import PrivateMediaStorage
from django.utils.translation import gettext_lazy as _
from django.core.mail import (
    EmailMultiAlternatives,
    EmailMessage,
    get_connection,
    message,
)
from apps.core.utils import default_from_email_sendinblue, connection


validators = [
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "png",
                    "jpeg",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ]


class Prequalification(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("final", "Published"),
    )

    company = models.ForeignKey('buyer.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='approved_by')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='created_by')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="draft")
    criteria_country = models.ForeignKey('core.CriteriaCountry', on_delete=models.CASCADE)
    old_system = models.BooleanField(default=False)
    show_bids = models.BooleanField(default=False)
    lang_en = models.BooleanField(default=False)
    advert = models.FileField(
        upload_to="job/advert", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=3000,
    )
    current_suppliers_letter = models.FileField(
        upload_to="job/current_suppliers_letter", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=3000,
    )
    current_suppliers = models.FileField(
        upload_to="job/current_suppliers", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=3000,
    )
    category_suppliers = models.FileField(
        upload_to="job/category_suppliers", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=3000,
    )
    bidding_instructions = models.FileField(
        upload_to="job/bidding_instructions", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=3000,
    )
    question_template = models.FileField(
        upload_to="prequal/job/questions/template/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=1000,
        # storage=PrivateMediaStorage(),
    )

    class Meta:
        verbose_name = "Prequalification"
        verbose_name_plural = "Prequalifications"

    @property
    def categories(self):
        return Category.objects.filter(prequalification_id=self.id)


class Category(BaseModel):
    name = models.CharField(max_length=1000)
    trans_name = models.CharField(max_length=1000, null=True, blank=True)
    unique_reference = models.CharField(max_length=1000, unique=True)
    bid_charge = models.DecimalField(max_digits=20, decimal_places=2)
    pass_score = models.IntegerField(default=70)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    evaluation_date = models.DateTimeField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    is_open = models.BooleanField(default=False)
    invite_only = models.BooleanField(default=False, blank=True, null=True)
    invite_notification = models.BooleanField(default=False)
    allowed_staff = models.BooleanField(default=False, blank=True, null=True)
    update_docs = models.BooleanField(default=False)
    send_participant_list_to_supplier = models.BooleanField(default=False, blank=True, null=True)
    parent_category = models.ForeignKey('Category', blank=True, null=True, on_delete=models.CASCADE)
    prequalification = models.ForeignKey(Prequalification, on_delete=models.CASCADE)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    question_template = models.FileField(
        upload_to="prequal/category/questions/template/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=1000,
        # storage=PrivateMediaStorage(),
    )

    class Meta:
        verbose_name = "Prequalification Category"
        verbose_name_plural = "Prequalification Categories"

    @property
    def company(self):
        return self.prequalification.company

    @property
    def suppliers_in_qa(self):
        qa = QualityAssurance.objects.filter(category_id=self.id).first()
        suppliers = Supplier.objects.filter(
            id__in=QualityAssuranceResponse.objects.filter(
            quality_assurance_question__quality_assurance_id=qa.id
        ).only('supplier_id').values('supplier_id').distinct()
        )
        return suppliers.count()

    @property
    def withdrawn_bids(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        category_orders_count = category_order.objects.filter(
            category_id=self.id, payment_status=category_order.WITHDRAW, target__model='category', target__app_label='prequal',
        ).count()
        return category_orders_count

    @property
    def withdrawn_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        suppliers = Supplier.objects.filter(
                id__in=category_order.objects.filter(
                category_id=self.id, payment_status=category_order.WITHDRAW, target__model='category', target__app_label='prequal',
            ).only("supplier_id").values("supplier_id").distinct()
        )
        return suppliers

    @property
    def responsive_bidders(self):
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        )
        return responsive

    @property
    def responsive_bidder_count(self):
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        ).count()
        return responsive

    @property
    def non_responsive_bids(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        category_orders_count = category_order.objects.filter(
            category_id=self.id, payment_status=category_order.PAID, target__model="prequalification"
        ).count()
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        ).count()
        return category_orders_count - responsive

    @property
    def non_responsive_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        all = Supplier.objects.filter(
                id__in=category_order.objects.filter(
                category_id=self.id, payment_status=category_order.PAID, target__model='category', target__app_label='prequal',
            ).only("supplier_id").values("supplier_id").distinct()
        )
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        )
        return all.difference(responsive)

    @property
    def worst_score(self):
        score = SupplierCategoryScore.objects.filter(category_id=self.id).order_by('score').first()
        if score:
            return score.score
        else:
            return ""

    @property
    def best_score(self):
        score = SupplierCategoryScore.objects.filter(category_id=self.id).order_by('-score').first()
        if score:
            return score.score
        else:
            return ""

    @property
    def average_score(self):
        # verify authenticity
        score = SupplierCategoryScore.objects.filter(category_id=self.id).annotate(avg=Avg('score')).first()
        if score:
            return score.avg
        else:
            return ""

    @property
    def questions(self):
        return Question.objects.filter(section__category_id=self.id)

    @property
    def sections(self):
        return Section.objects.filter(category_id=self.id)

    @property
    def total_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        total_bidders = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=category_order.objects.filter(
                payment_status=category_order.PAID, category_id=self.id, target__model='category', target__app_label='prequal',
            ).only('supplier_id').values('supplier_id').distinct()
        )
        return total_bidders.count()

    @property
    def paid_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        supplier_ids = category_order.objects.filter(
                payment_status=category_order.PAID, category_id=self.id, target__model='category', target__app_label='prequal',
            ).only('supplier_id').values('supplier_id')
        bidders = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=supplier_ids
        )
        return bidders

    @property
    def count_qualified_bidders(self):
        totals = SupplierCategoryScore.objects.filter(category_id=self.id, score__gte=self.pass_score)
        return totals.count()

    @property
    def qualified_bidders(self):
        suppliers = apps.apps.get_model("suppliers", "Supplier").objects.filter(
            id__in=SupplierCategoryScore.objects.filter(
                category_id=self.id, score__gte=self.pass_score).only('supplier_id').values('supplier_id')
        )
        return suppliers

    @property
    def unqualified_bidders(self):
        suppliers = apps.apps.get_model("suppliers", "Supplier").objects.filter(
            id__in=SupplierCategoryScore.objects.filter(
                category_id=self.id, score__lt=self.pass_score).only('supplier_id').values('supplier_id')
        )
        return suppliers

    @property
    def participants(self):
        suppliers = []
        scores = SupplierCategoryScore.objects.filter(category_id=self.id).order_by(
            "-score"
        )
        if scores.count() == 0:
            suppliers = Supplier.objects.filter(
                id__in=SupplierResponse.objects.filter(
                    question__section__category_id=self.id).only("supplier_id").values("supplier_id").distinct()
            )
            # todo calculate category scores
            return suppliers
        else:
            for score in scores:
                suppliers.append(score.supplier)
            # is here to check  for those who  submitted in sections that dont have a score thus wont be having a Prequalscore

            s_suppliers = Supplier.objects.filter(
                id__in=SupplierResponse.objects.filter(
                    question__section__category_id=self.id).only("supplier_id").values("supplier_id").distinct()
            )

            for supplier in s_suppliers:
                if supplier not in suppliers:
                    suppliers.append(supplier)

            return set(suppliers)

    def sorted_participants_by_qa(self, participants=None):
        sorted_participants = []
        first_score = SupplierCategoryScore.objects.filter(category_id=self.id).first()
        if first_score is None:
            # get a first score by calculating rfq scores for each participant
            if participants is None:
                participants = self.participants
            for participant in participants:
                participant.resolve_qa_scores(self)
            first_score = SupplierCategoryScore.objects.filter(
                prequal_id=self.id
            ).first()
            if first_score is not None:
                if first_score.rank_after_qa is None or first_score.rank_after_qa == 0:
                    self.qa_rank_participants()
        else:
            if first_score.rank_after_qa is None or first_score.rank_after_qa == 0:
                self.qa_rank_participants()

        scores = SupplierCategoryScore.objects.filter(category_id=self.id).order_by(
            "rank_after_qa"
        )

        for score in scores:
            sorted_participants.append(score.supplier)
        return sorted_participants

    def rank_participants(self):
        scores = SupplierCategoryScore.objects.filter(category_id=self.id).order_by(
            "-prequal_score"
        )
        rank = 0
        first_score = scores.first()
        if first_score is not None:
            first_score.rank = 1
            first_score.save()
            prev_score = first_score
            for prequal_score in scores:
                if prequal_score.prequal_score == prev_score.prequal_score:
                    prequal_score.rank = prev_score.rank
                else:
                    prequal_score.rank = rank + 1
                rank += 1
                prequal_score.save()
                prev_score = prequal_score
        return True

    def qa_rank_participants(self):
        scores = SupplierCategoryScore.objects.filter(category_id=self.id).order_by(
            "-score_after_qa"
        )
        rank_after_qa = 0
        if scores.first().score_after_qa is not None:
            first_score = scores.first()
        else:
            first_score = scores[1]

        if first_score is not None:
            first_score.rank_after_qa = 1
            first_score.save()
            prev_score = first_score
            for prequal_score in scores:
                if prequal_score.score_after_qa == None:
                    prequal_score.rank_after_qa = None
                    rank_after_qa += 0
                    prequal_score.save()
                    continue
                elif prequal_score.score_after_qa == prev_score.score_after_qa:
                    prequal_score.rank_after_qa = prev_score.rank_after_qa
                else:
                    prequal_score.rank_after_qa = rank_after_qa + 1
                rank_after_qa += 1
                prequal_score.save()
                prev_score = prequal_score
        return True

    # def get_supplier_progress(self):
    #     category_orders = apps.apps.get_model('core', 'CategoryOrder').objects.filter(category=self)
    #     non_progressive = []
    #
    #     participants = self.participants
    #     for participant in participants:
    #         answered = participant.count_answered_questions(self.id)
    #         total = len(self.questions)
    #         progress = round((answered / total) * 100, 1)
    #
    #         order = category_orders.filter(
    #             category=self, supplier_profile__supplier=participant
    #         ).first()
    #         if order:
    #             today = datetime.datetime.now(timezone.utc)
    #             closing_date = self.closing_date
    #             payment_date = order.payment_date
    #             time_diff = closing_date - today
    #
    #         if progress < 100.0:
    #             if int(time_diff.days) == 7 or int(time_diff.days) == 3:
    #                 non_progressive_data = {
    #                     "supplier": participant,
    #                     "progress": progress,
    #                 }
    #                 non_progressive.append(non_progressive_data)
    #
    #         else:
    #             pass
    #     return non_progressive

    # @property
    # def get_suppliers(self):
    #     company_suppliers = Supplier.objects.filter(
    #         id__in=CompanySupplier.objects.filter(
    #             company__company__category=self, company_id=self.company
    #         ).only('supplier_id').values('supplier_id')
    #     ).order_by('id')
    #     return company_suppliers

    def validate_phone_number(self, phone_number, country=None):
        if country == None or country == "Kenya":
            reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
            reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
            reg2 = re.compile(r"^[0]\d{9}$")
            reg3 = re.compile(r"^[7]\d{8}$")
            phone_number = re.sub(r"\s+", "", phone_number)
            if reg.search(phone_number):
                return phone_number
            elif reg1.search(phone_number):
                phone_number = phone_number.replace("+", "")
                return phone_number
            elif reg2.search(phone_number):
                phone_number = re.sub(phone_number[0], "254", phone_number, 1)
                return phone_number
            elif reg3.search(phone_number):
                phone_number = "254" + phone_number[:9]
                return phone_number
            else:
                return False
        else:
            HC = apps.apps.get_model("core", "HelpContact").objects.get(country=country)
            calling_code = HC.country_calling_code
            reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
            reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
            reg2 = re.compile(r"^[0]\d{9}$")
            reg3 = re.compile(r"^[7]\d{8}$")
            phone_number = re.sub(r"\s+", "", phone_number)
            try:
                if reg.search(phone_number):
                    return phone_number
                elif reg1.search(phone_number):
                    phone_number = phone_number.replace("+", "")
                    return phone_number
                elif reg2.search(phone_number):
                    phone_number = re.sub(
                        phone_number[0], calling_code, phone_number, 1
                    )
                    return phone_number
                elif reg3.search(phone_number):
                    phone_number = calling_code + phone_number[:9]
                    return phone_number
                else:
                    return False
            except Exception as e:
                capture_exception(e)

    def invite_suppliers_sms(self, supplier_phone_number, count, country=None):
        api_url = "http://52.15.88.116/bulkAPIV2/"
        valid_phone_number = self.validate_phone_number(supplier_phone_number, country)
        if valid_phone_number:
            try:
                request_sms = {
                    # "user": settings.MTECH_API_USER,
                    # "pass": settings.MTECH_API_PASS,
                    "message": f"Tendersure is managing the prequalification for {self.job.company}.Closing date {self.closing_date.date()}.To bid go to www.tendersure.co.ke and click 'Available Jobs'",
                    "msisdn": valid_phone_number,
                    # "shortCode": settings.MTECH_API_SHORTCODE,
                    "messageID": f"{ self.name }" + f"{ count }",
                    "coding": "utf-8",
                }
                response = requests.get(api_url, params=request_sms)
            except Exception as e:
                capture_exception(e)


class Section(BaseModel):
    name = models.CharField(max_length=3000, db_index=True)
    trans_name = models.CharField(max_length=3000, blank=True, null=True)
    short_name = models.CharField(max_length=3000, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    parent_section = models.ForeignKey(
        "Section", blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    name_slug = SlugField(blank=True, null=True, max_length=30000)

    class Meta:
        verbose_name = "Section"
        verbose_name_plural = "Sections"

    def __str__(self):
        return f"{self.name} ({self.id})"

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    @property
    def has_child_sections(self):
        if Section.objects.filter(parent_section_id=self.id).count() > 0:
            return True
        else:
            return False

    @property
    def child_sections(self):
        return Section.objects.filter(parent_section=self).order_by("id")

    @property
    def is_scored(self):
        questions = Question.objects.filter(section_id=self.id, is_scored=True)
        if questions.count() > 0:
            return True
        else:
            return False

    @property
    def is_parent_section_scored(self):
        if self.is_scored:
            return True
        else:
            if self.has_child_sections:
                for s in self.child_sections:
                    s.is_parent_section_scored()
            else:
                return False

    @property
    def section_score(self):
        questions = Question.objects.filter(section_id=self.id, is_scored=True).annotate(section_score=Sum('max_score'))
        if questions:
            return questions.first().section_score
        return 0

    @property
    def questions(self):
        return Question.objects.filter(section_id=self.id)

    def supplier_financial_ratio_score(self, supplier):
        if self.name == "Financial Ratios":
            all_questions = Question.objects.filter(section_id=self.id).order_by("id")
            first_question = all_questions.first()
            other_questions = all_questions.exclude(id=first_question.id)
            supplier_responses = SupplierResponse.objects.filter(
                supplier_id=supplier.id, question__section_id=self.id
            )
            score = 0

            ac_question = Question.objects.filter(
                description="1. For limited liability companies, attach audited accounts for the last two years, "
                            "for sole proprietors and partnerships, attach your most recent management accounts",
                section__category_id=self.category_id
            ).first()

            if ac_question is not None:
                supplier_response = SupplierResponse.objects.filter(question_id=ac_question.id,
                                                                    supplier_id=supplier.id).first()

                if supplier_response is None:
                    return score
                elif supplier_response is not None:
                    if supplier_response.options is None and supplier_response.document_url is None:
                        return score
                    else:
                        for question in other_questions:
                            question_options = question.options
                            response = supplier_responses.filter(question_id=question.id).first()

                            if response is not None:
                                for option in question_options:
                                    start = float(option.split("-", 1)[0])
                                    end = float(option.split("-", 1)[1])
                                    q_ratio = math.floor(float(response.options) * 10) / 10

                                    if start <= q_ratio <= end:
                                        my_index = question_options.index(option)
                                        s = float(question.scores[my_index])
                                        score += s
                                        break
                                    else:
                                        continue
                        return score
                else:
                    return score
            return score
        else:
            return


class Question(BaseModel):
    TYPE_TEXT = 1
    TYPE_SELECT = 2
    TYPE_CHECKBOX = 3
    TYPE_BOOLEAN = 4
    TYPE_UPLOAD = 5
    TYPE_NUMBER = 6
    TPE_DATE = 7
    TYPE_TEXTBOX = 8

    ANSWER_TYPE_CHOICES = (
        (TYPE_TEXT, _("Text")),
        (TYPE_SELECT, _("Select")),
        (TYPE_CHECKBOX, _("Checkbox")),
        (TYPE_BOOLEAN, _("Boolean")),
        (TYPE_UPLOAD, _("File Upload")),
        (TYPE_NUMBER, _("Number")),
        (TPE_DATE, _("Date")),
        (TYPE_TEXTBOX, _("Textbox")),
    )

    TYPE_IN_WORDS = {
        TYPE_TEXT: _("Text"),
        TYPE_SELECT: _("Selection"),
        TYPE_CHECKBOX: _("Checkboxes"),
        TYPE_BOOLEAN: _("True/False"),
        TYPE_UPLOAD: _("File Upload"),
        TYPE_NUMBER: _("Number"),
        TPE_DATE: _("Date"),
        TYPE_TEXTBOX: _("Textbox"),
    }

    answer_type = models.IntegerField(
        choices=ANSWER_TYPE_CHOICES, default=TYPE_TEXT, blank=False, null=False
    )
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    description = models.TextField(max_length=30000)
    trans_description = models.TextField(max_length=30000, blank=True, null=True)
    short_description = models.TextField(max_length=30000, blank=True, null=True)
    trans_short_description = models.TextField(max_length=30000, blank=True, null=True)
    is_required = models.BooleanField(
        default=False,
    )
    max_score = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, default=0, null=True
    )
    is_scored = models.BooleanField(default=True)
    is_qa = models.BooleanField(default=False)
    is_dd = models.BooleanField(default=False)
    description_slug = models.SlugField(blank=True, null=True, max_length=30000)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return (
            self.section.category.unique_reference + " - "
            + str(self.section.short_name) + " - " + str(self.id)
        )

    def save(self, *args, **kwargs):
        self.description_slug = slugify(self.description)
        super(Question, self).save(*args, **kwargs)

    @property
    def marking_scheme(self):
        if MarkingScheme.objects.filter(question=self).count() > 0:
            return MarkingScheme.objects.filter(question=self).first()
        return None

    @property
    def options(self):
        if self.marking_scheme:
            return self.marking_scheme.options.split(",")
        else:
            return []

    @property
    def scores(self):
        if self.marking_scheme:
            return self.marking_scheme.score.split(",")
        else:
            return []

    def supplier_financial_ratio_score(self, supplier):
        supplier_responses = SupplierResponse.objects.filter(
            supplier_id=supplier.id, question_id=self.id
        )

        score = 0
        question_options = self.options
        response = supplier_responses.filter(question_id=self.id).first()

        ac_question = Question.objects.filter(
            description="1. For limited liability companies, attach audited accounts for the last two years, "
                        "for sole proprietors and partnerships, attach your most recent management accounts",
            section__category_id=self.section.category_id
        ).first()

        if ac_question is not None:
            supplier_response = SupplierResponse.objects.filter(question_id=ac_question.id,
                                                                supplier_id=supplier.id).first()
            if supplier_response is None:
                return score
            elif supplier_response is not None:
                if supplier_response.options is None and supplier_response.document_url is None:
                    return score
                else:
                    if response is not None:
                        for option in question_options:
                            start = float(option.split("-", 1)[0])
                            end = float(option.split("-", 1)[1])
                            q_ratio = math.floor(float(response.options) * 10) / 10

                            if start <= q_ratio <= end:
                                my_index = question_options.index(option)
                                s = float(self.scores[my_index])
                                score = s
                                break
                            else:
                                continue
                    return score
            else:
                return score
        return score


class MarkingScheme(BaseModel):
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    options = models.TextField(default="", db_index=True, max_length=30000)
    # options = models.TextField(blank=True, null=True, default="")
    score = models.TextField(default="", db_index=True, max_length=30000)

    class Meta:
        verbose_name = "Marking Scheme"
        verbose_name_plural = "Marking Schemes"


class SupplierResponse(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,
        related_name="supplier_response", on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to=supplier_response_files, validators=validators,
        blank=True, null=True, max_length=1000,
        storage=PrivateMediaStorage(),
    )
    options = pgcrypto.EncryptedTextField(
        max_length=100000, db_index=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Supplier Response"
        verbose_name_plural = "Supplier Responses"

    @property
    def document_response_url(self):
        question = Question.objects.filter(id=self.question.id).first()
        response = None
        if question is not None:
            supplier_response = SupplierResponse.objects.filter(
                question=question, supplier=self.supplier.id
            ).first()
            if supplier_response is not None:
                if supplier_response.document_url:
                    response = supplier_response.document_url.url
                elif len(supplier_response.options) > 6:
                    response = get_document_url(f"{supplier_response.options}")
                else:
                    pass
        return response


class QualityAssurance(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    title = models.CharField(max_length=250)

    class Meta:
        verbose_name = "Quality Assurance"
        verbose_name_plural = "Quality Assurances"

    def __str__(self):
        return self.title


class QualityAssuranceQuestion(BaseModel):
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    quality_assurance = models.ForeignKey(
        QualityAssurance, blank=False, null=False, on_delete=models.CASCADE
    )
    verification_instruction = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Quality Assurance Question"
        verbose_name_plural = "Quality Assurance Questions"


class QualityAssuranceResponse(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))
    SEVERITY_CHOICES = (("High", "High"), ("Medium", "Medium"), ("Low", "Low"))

    CREATED = 1
    VERIFIED = 2

    VERIFICATION_STATUS_CHOICES = (
        (CREATED, "Created"),
        (VERIFIED, "Verified"),
    )

    supplier = models.ForeignKey(
        Supplier, on_delete=models.CASCADE
    )
    quality_assurance_question = models.ForeignKey(
        QualityAssuranceQuestion, on_delete=models.CASCADE
    )
    number = models.CharField(max_length=200, null=True, blank=True)
    date = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    outcome = models.CharField(
        max_length=200, choices=STATUS_CHOICES, default="outcome", null=True, blank=True
    )
    severity = models.CharField(
        max_length=200, choices=SEVERITY_CHOICES, default="severity", null=True, blank=True
    )
    document = models.FileField(
        upload_to="Rfq/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True,
        null=True, max_length=1000,
    )
    score_after_qa = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True, default=0
    )
    created_by = models.ForeignKey(
        User, blank=False, related_name="response_created_by",
        null=True, on_delete=models.CASCADE,
    )
    verified_by = models.ForeignKey(
        User, blank=True, related_name="response_verified_by",
        null=True, on_delete=models.CASCADE,
    )
    status = models.IntegerField(choices=STATUS_CHOICES, default=CREATED)
    ocr_response = models.JSONField(null=True, blank=True)

    class Meta:
        verbose_name = "Quality Assurance Response"
        verbose_name_plural = "Quality Assurance Responses"

    def __str__(self):
        return (
            self.supplier.company_name + " - " + str(self.score_after_qa)
            + " - " + self.outcome
        )


class QaTccResponse(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    pin_number = models.CharField(max_length=250, null=True, blank=True)
    pin_number_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, null=True, blank=True)
    company_name = models.CharField(max_length=250, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    expiry_date_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11)

    class Meta:
        verbose_name = "Qa Tcc Response"
        verbose_name_plural = "Qa Tcc Responses"


class QaIncorporationCertificateResponse(BaseModel): # Registration Certificate
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    company_number = models.CharField(max_length=250, null=True, blank=True)
    company_number_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, null=True, blank=True)
    company_name = models.CharField(max_length=250, null=True, blank=True)
    company_name_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, null=True, blank=True)

    class Meta:
        verbose_name = "Qa Incorporation Certificate Response"
        verbose_name_plural = "Qa Incorporation Certificate Responses"


class QaCr12Response(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    company_number = models.CharField(max_length=250, null=True, blank=True)
    company_number_outcome = models.CharField(max_length=11, choices=STATUS_CHOICES, null=True, blank=True)
    directors = models.JSONField(null=True, blank=True)
    directors_outcome = models.CharField(max_length=11, choices=STATUS_CHOICES, null=True, blank=True)
    document_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Qa Cr12 Response"
        verbose_name_plural = "Qa Cr12 Responses"


class QaBusinessPermitResponse(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=250, null=True, blank=True)
    business_name_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, null=True, blank=True)
    business_id = models.CharField(max_length=250, null=True, blank=True)
    date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Qa Business Permit Response"
        verbose_name_plural = "Qa Business Permit Responses"


class QaNcaaResponse(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    serial_number = models.CharField(max_length=250, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    expiry_date_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = "Qa Ncaa Response"
        verbose_name_plural = "Qa Ncaa Responses"


class QaPoisonsBoardResponse(BaseModel): # License
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=250, null=True, blank=True)
    company_name_outcome = models.CharField(choices=STATUS_CHOICES, max_length=250, null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    expiry_date_outcome = models.CharField(choices=STATUS_CHOICES, max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Qa Poisons Board Response"
        verbose_name_plural = "Qa Poisons Board Responses"


class QaNationalIdResponse(BaseModel):
    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True, blank=True)
    id_number = models.CharField(max_length=250, null=True, blank=True)

    class Meta:
        verbose_name = "Qa National Id Response"
        verbose_name_plural = "Qa National Id Responses"


class QaPinCertificateResponse(BaseModel):
    STATUS_CHOICES = (("Pass", "Pass"), ("Fail", "Fail"), ("Subjective", "Subjective"))

    qa_response = models.ForeignKey(QualityAssuranceResponse, on_delete=models.CASCADE)
    pin_number = models.CharField(max_length=250, null=True, blank=True)
    tax_pin_outcome = models.CharField(choices=STATUS_CHOICES, max_length=11, blank=True, null=True)

    class Meta:
        verbose_name = "Qa Pin Certificate Response"
        verbose_name_plural = "Qa Pin Certificate Responses"


class DueDiligence(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    created_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Due Diligence"
        verbose_name_plural = "Due Diligence"

    def __str__(self):
        return self.category.name


class DueDiligenceSupplier(BaseModel):
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    due_diligence = models.ForeignKey(
        DueDiligence, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Due Diligence Supplier"
        verbose_name_plural = "Due Diligence Suppliers"


class DueDiligenceQuestion(BaseModel):
    due_diligence_supplier = models.ForeignKey(
        DueDiligenceSupplier, blank=False, null=False, on_delete=models.CASCADE
    )
    question = models.TextField()
    due_diligence_response = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Due Diligence Question"
        verbose_name_plural = "Due Diligence Questions"


class SupplierSectionScore(BaseModel):
    section = models.ForeignKey(
        Section, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    score = models.BigIntegerField(null=True, blank=True)
    score_after_qa = models.BigIntegerField(null=True, blank=True)


class SupplierCategoryScore(BaseModel):
    meets_all_mandatory_requirements = models.BooleanField(null=True, blank=True)
    technically_qualified = models.BooleanField(null=True, blank=True)
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    score = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, default=0
    )
    score_after_qa = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, null=True, blank=True
    )
    # # weighted score
    # prequal_score = models.DecimalField(
    #     max_digits=20, decimal_places=6, db_index=True, default=0
    # )
    rank = models.BigIntegerField(db_index=True, default=0)
    rank_after_qa = models.BigIntegerField(db_index=True, null=True, blank=True)


class CategoryReport(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    bidder_information = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        blank=True, null=True,
        storage=PrivateMediaStorage()
    )
    technical_evaluation_summary = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation_responses = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_pdf = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_excel = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    dd = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    financial_ratios = models.FileField(
        upload_to="prequal/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )

    class Meta:
        verbose_name = "Prequal Report"
        verbose_name_plural = "Prequal Reports"


# models related to letters
class AwardLetter(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    award_date = models.DateTimeField()
    letter = models.FileField(
        upload_to=supplier_letters,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Award Letter"
        verbose_name_plural = "Award Letters"

    def __str__(self):
        return self.name

    @property
    def full_document_url(self):
        response = None
        if self.letter:
            response = get_document_url(f"{self.letter}")
        return response


class CategorySupplierPayment(BaseModel):
    PAID = 1
    REFUNDED = 2

    STATUS_CHOICES = ((PAID, "Paid"), (REFUNDED, "Refunded"))

    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    # payment = models.ForeignKey(
    #     Payment, blank=False, null=False, on_delete=models.CASCADE
    # )
    status = models.IntegerField(
        choices=STATUS_CHOICES, default=PAID, blank=False, null=False
    )

    class Meta:
        verbose_name = "Category Supplier"
        verbose_name_plural = "Categories Suppliers"


class RegretLetter(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category_supplier = models.ForeignKey(
        CategorySupplierPayment, blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    regret_date = models.DateTimeField()
    letter = models.FileField(
        upload_to=supplier_letters,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Regret Letter"
        verbose_name_plural = "Regret Letters"

    def __str__(self):
        return self.name

    @property
    def full_document_url(self):
        response = None
        if self.letter:
            response = get_document_url(f"{self.letter}")
        return response


class DueDilligenceLetter(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category_supplier = models.ForeignKey(
        CategorySupplierPayment, blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    due_dilligence_letter_date = models.DateTimeField()
    letter = models.FileField(
        upload_to=supplier_letters,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Due Dilligence Letter"
        verbose_name_plural = "Due Dilligence Letters"

    def __str__(self):
        return self.name

    @property
    def full_document_url(self):
        response = None
        if self.letter:
            response = get_document_url(f"{self.letter}")
        return response


class CustomLetter(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    category_supplier = models.ForeignKey(
        CategorySupplierPayment, blank=True, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE
    )
    custom_letter_date = models.DateTimeField()
    letter = models.FileField(
        upload_to=supplier_letters,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Custom Letter"
        verbose_name_plural = "Custom Letters"

    def __str__(self):
        return self.name

    @property
    def full_document_url(self):
        response = None
        if self.letter:
            response = get_document_url(f"{self.letter}")
        return response


class SupplierPDFResponse(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier,
        related_name="supplier_pdf_response",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to="supplier_PDF_responses",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "png",
                    "jpeg",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
        db_column='document_url'
    )

    class Meta:
        verbose_name = "Supplier PDF Response"
        verbose_name_plural = "Supplier PDF Responses"

    def __str__(self):
        return self.supplier.username

    @property
    def full_document_url(self):
        response = None
        if self.document_url:
            response = get_document_url(f"{self.document_url}")
        return response


class JobReport(BaseModel):
    prequalification = models.ForeignKey(Prequalification, on_delete=models.CASCADE)
    interim_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    qa_ranking_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    bidder_locations_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    prequalified_suppliers_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    bidder_payments_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    responsive_bidders_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    non_responsive_bidders_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    directors_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    participation_status_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    dd_ranking_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    category_suppliers_report = models.FileField(
        upload_to="prequal/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )

    class Meta:
        verbose_name = "Job Report"
        verbose_name_plural = "Job Reports"


class CategoryInvite(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.CASCADE)
    # add a field to indicate whether email was sent

    class Meta:
        verbose_name = "Category Invite"
        verbose_name_plural = "Category Invites"


class FinancialRatio(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    equity = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    curr_liabilities = models.DecimalField(help_text="Current Liabilities", max_digits=15, decimal_places=2, blank=True,null=True)
    fixed_assets = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    current_assets = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    debtors = models.DecimalField(help_text="Long Term Loans",max_digits=15, decimal_places=2,null=True)
    turnover = models.DecimalField(help_text="Sales", max_digits=15, decimal_places=2,null=True)
    gross_profit = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    net_profit = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    cash = models.DecimalField(max_digits=15, decimal_places=2,null=True)
    equity_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    curr_liabilities_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    fixed_assets_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    current_assets_after_qa = models.DecimalField(max_digits=15,decimal_places=2, blank=True, null=True)
    debtors_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    turnover_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    gross_profit_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    net_profit_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    cash_after_qa = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name = "FinancialRatio"
        verbose_name_plural = "FinancialRatios"

    def __str__(self):
        return f"{self.supplier.company_name} {self.section.category.name}"


class QuestionArchive(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier,
        related_name="prequal_question_archive",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to=supplier_response_files,
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "jpg",
                    "png",
                    "jpeg",
                    "xlsx",
                    "xls",
                    "zip",
                    "rar",
                ]
            )
        ],
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Question Archive"
        verbose_name_plural = "Questions Archive"


class ClientDocument(BaseModel):
    """
    Custom model to store different documents to be sent to the supplier.
    """
    SUCCESS = 'success'
    REGRET = 'regret'
    DD = 'dd'
    CUSTOM = 'custom'
    DOCUMENT_TYPES = (
        (SUCCESS, 'success'),
        (REGRET, 'regret'),
        (DD, 'dd'),
        (CUSTOM, 'custom')
    )
    prequalification = models.ForeignKey(
        Prequalification, blank=True, null=True, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=200, choices=DOCUMENT_TYPES)
    tendersure_module = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    authoriser_name = models.CharField(max_length=200, blank=True, null=True)
    authoriser_role = models.CharField(max_length=200, blank=True, null=True)
    header = models.ImageField(
        upload_to="buyer_documents/%Y/%m/%d",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "gif"])],
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    footer = models.ImageField(
        upload_to="buyer_documents/%Y/%m/%d",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "gif"])
        ],
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    signature = models.ImageField(
        upload_to="buyer_documents/%Y/%m/%d",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "gif"])
        ],
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    watermark = models.ImageField(
        upload_to="buyer_documents/%Y/%m/%d",
        validators=[
            FileExtensionValidator(allowed_extensions=["jpg", "png", "jpeg", "gif"])
        ],
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    file = models.FileField(
        upload_to="buyer_documents/%Y/%m/%d",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf", "doc", "docx", "jpg", "png", "jpeg",
                    "xlsx", "xls", "zip", "rar"])],
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )
    subject = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Client Document"
        verbose_name_plural = "Client Documents"

    
class SupplierBuyerNotification(BaseModel):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    buyer = models.ForeignKey('buyer.Buyer', on_delete=models.CASCADE)
    job = models.ForeignKey(Prequalification, on_delete=models.CASCADE)
    email_subject = models.TextField()
    email_body = models.TextField()
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return (
            f"{self.supplier.company_name} & {self.buyer.company.company_name} emails"
        )