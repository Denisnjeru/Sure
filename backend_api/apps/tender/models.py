import datetime
import re
import statistics

import pgcrypto
import requests
from django import apps
from django.contrib.auth.models import User
from django.db import models
from django.db.models import SlugField, Sum, Avg
from django.template.defaultfilters import slugify
from django.utils import timezone
from sentry_sdk import capture_exception

from apps.core.models import BaseModel, CategoryType, Currency
from django.core.validators import FileExtensionValidator

from apps.core.utils import show, get_document_url
from apps.tender.utils import supplier_response_files, supplier_letters
from apps.suppliers.models import Supplier
from backend.storage_backends import PrivateMediaStorage
from django.utils.translation import gettext_lazy as _


validators = [
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf", "doc", "docx", "jpg", "png", "jpeg", "xlsx", "xls", "zip", "rar",
                ]
            )
        ]


class Tender(BaseModel):
    MULTI_ITEM = 1
    CONSOLIDATED = 2

    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("final", "Published"),
    )
    TYPE_CHOICES = ((MULTI_ITEM, "Multi-Item"), (CONSOLIDATED, "Consolidated"))

    company = models.ForeignKey('buyer.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    approved_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='tender_approved_by')
    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name='tender_created_by')
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="draft")
    old_system = models.BooleanField(default=False)
    show_bids = models.BooleanField(default=False)
    lang_en = models.BooleanField(default=False)
    type = models.IntegerField(choices=TYPE_CHOICES, null=True, blank=True)
    criteria_country = models.ForeignKey('core.CriteriaCountry', related_name='tender_criteria', on_delete=models.CASCADE)
    advert = models.FileField(
        upload_to="job/advert", validators=validators,
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
        upload_to="job/questions/template/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=1000,
        # storage=PrivateMediaStorage(),
    )

    class Meta:
        verbose_name = "Tender"
        verbose_name_plural = "Tenders"

    @property
    def categories(self):
        return Category.objects.filter(tender_id=self.id)


class Category(BaseModel):
    RFQ_CHOICES = (
        ("basic", "Basic"),
        ("advanced", "Advanced"),
    )
    name = models.CharField(max_length=1000)
    trans_name = models.CharField(max_length=1000, null=True, blank=True)
    unique_reference = models.CharField(max_length=1000)
    bid_charge = models.DecimalField(max_digits=20, decimal_places=2)
    pass_score = models.IntegerField(default=70)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    evaluation_date = models.DateTimeField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name="tender_currency")
    is_open = models.BooleanField(default=False)
    invite_only = models.BooleanField(default=False)
    invite_notification = models.BooleanField(default=False)
    self_evaluate = models.BooleanField(default=True)
    allowed_staff = models.BooleanField(default=False)
    update_docs = models.BooleanField(default=False)
    send_participant_list_to_supplier = models.BooleanField(default=False)
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE, related_name="tender_category_type")
    technical_weight = models.DecimalField(max_digits=15, decimal_places=2, default=70)
    financial_weight = models.DecimalField(max_digits=15, decimal_places=2, default=30)
    total_savings = models.FloatField(default=0, null=True, blank=True)
    rfq_type = models.CharField(choices=RFQ_CHOICES, max_length=10, default="basic")
    vatable = models.BooleanField(default=True)
    vat_rate = models.FloatField(default=16.0, null=True, blank=True)
    question_template = models.FileField(
        upload_to="prequal/category/questions/template/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=1000,
        # storage=PrivateMediaStorage(),
    )
    items_template = models.FileField(
        upload_to="Rfq/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
        max_length=1000)
    current_prices_template = models.FileField(
        upload_to="Tender/current_prices/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
        max_length=2000)

    class Meta:
        verbose_name = "Tender Category"
        verbose_name_plural = "Tender Categories"

    @property
    def company(self):
        return self.tender.company

    @property
    def technical_participants(self):
        suppliers = []
        scores = SupplierTechnicalScore.objects.filter(category_id=self.id).order_by(
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

    @property
    def sorted_technical_participants(self):
        suppliers = []
        scores = SupplierTechnicalScore.objects.filter(category_id=self.id).order_by(
            "-score"
        )
        for score in scores:
            suppliers.append(score.supplier)
        return suppliers

    @property
    def sorted_successful_participants(self):
        sorted_participants = []

        scores = SupplierCategoryScore.objects.filter(category_id=self.id).extra(
            select={
                "not_ranked": "rank = 0",
            },
            order_by=["not_ranked", "rank"],
        )
        for score in scores:
            sorted_participants.append(score.supplier)

        return sorted_participants

    @property
    def invited_suppliers(self):
        suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=Invitee.objects.filter(
                category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        )
        return suppliers

    @property
    def total_technical_score(self):
        q = Question.objects.filter(section__category_id=self.id).aggregate(total_score=Sum('max_score')).first()
        if q:
            return q['total_score']
        else:
            return 0

    @property
    def suppliers_in_qa(self):
        qa = QualityAssurance.objects.filter(category_id=self.id).first()
        if qa:
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
            category_id=self.id, payment_status=category_order.WITHDRAW, target__model="tender"
        ).count()
        return category_orders_count

    @property
    def withdrawn_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        suppliers = Supplier.objects.filter(
            id__in=category_order.objects.filter(
                category_id=self.id, payment_status=category_order.WITHDRAW, target__model="tender"
            ).only("supplier_id").values("supplier_id").distinct()
        )
        return suppliers

    @property
    def responsive_bidders(self):
        # include financial
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        )
        return responsive

    @property
    def responsive_bidder_count(self):
        # include financial
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        ).count()
        return responsive

    @property
    def non_responsive_bids(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        category_orders_count = category_order.objects.filter(
            category_id=self.id, payment_status=category_order.PAID, target__model='category', target__app_label='tender',
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
                category_id=self.id, payment_status=category_order.PAID, target__model='category', target__app_label='tender',
            ).only("supplier_id").values("supplier_id").distinct()
        )
        responsive = Supplier.objects.filter(
            id__in=SupplierResponse.objects.filter(
                question__section__category_id=self.id).only('supplier_id').values('supplier_id').distinct()
        )
        return all.difference(responsive)

    @property
    def questions(self):
        return Question.objects.filter(section__category_id=self.id)

    @property
    def sections(self):
        return Section.objects.filter(category_id=self.id)

    @property
    def scored_sections(self):
        sections = Section.objects.filter(
            id__in=Question.objects.filter(
                section__category_id=self.id, is_qa=True, is_scored=True
            ).only('section_id').values('section_id').distinct()
        )
        # for section in Section.objects.filter(category_id=self.id):
        #     if Question.objects.filter(
        #             section_id=section.id, ).exists():
        #         sections.append(section)
        return sections

    @property
    def worst_score(self):
        score = SupplierTechnicalScore.objects.filter(category_id=self.id).order_by('score').first()
        if score:
            return score.score
        else:
            return ""

    @property
    def best_score(self):
        score = SupplierTechnicalScore.objects.filter(category_id=self.id).order_by('-score').first()
        if score:
            return score.score
        else:
            return ""

    @property
    def average_score(self):
        # verify authenticity
        score = SupplierTechnicalScore.objects.filter(category_id=self.id).annotate(avg=Avg('score')).first()
        if score:
            return score.avg
        else:
            return ""

    @property
    def total_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        total_bidders = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=category_order.objects.filter(
                payment_status=category_order.PAID, category_id=self.id, target__model='tender'
            ).only('supplier_id').values('supplier_id')
        )
        return total_bidders.count()

    @property
    def count_qualified_bidders(self):
        totals = SupplierTechnicalScore.objects.filter(category_id=self.id, score__gte=self.pass_score)
        return totals.count()

    @property
    def qualified_bidders(self):
        suppliers = apps.apps.get_model("suppliers", "Supplier").objects.filter(
            id__in=SupplierTechnicalScore.objects.filter(
                category_id=self.id, score__gte=self.pass_score).only('supplier_id').values('supplier_id')
        )
        return suppliers

    @property
    def unqualified_bidders(self):
        suppliers = apps.apps.get_model("suppliers", "Supplier").objects.filter(
            id__in=SupplierTechnicalScore.objects.filter(
                category_id=self.id, score__lt=self.pass_score).only('supplier_id').values('supplier_id')
        )
        return suppliers

    @property
    def paid_bidders(self):
        category_order = apps.apps.get_model('core', 'CategoryOrder')
        supplier_ids = category_order.objects.filter(
            payment_status=category_order.PAID, category_id=self.id, target__model='tender'
        ).only('supplier_id').values('supplier_id')
        bidders = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=supplier_ids
        )
        return bidders

    @property
    def financial_participants(self):
        suppliers = []
        tender_financial_scores = SupplierFinancialTotal.objects.filter(category_id=self.id).values_list(
            "supplier_id", flat=True
        )
        if tender_financial_scores.count() == 0:
            responses = ItemResponse.objects.filter(
                item__category_id=self.id
            )
            for response in responses:
                supplier = response.supplier
                if supplier not in suppliers:
                    suppliers.append(supplier)
            participants = set(suppliers)
            return {"participants": participants, "count": len(participants)}
        else:
            # participants = apps.get_model("suppliers.Supplier").objects.filter(
            #     id__in=rfq_scores.only("supplier_id").distinct("supplier_id")
            # )
            participants = apps.get_model("suppliers", "Supplier").objects.filter(
                id__in=tender_financial_scores
            )
            return {"participants": participants, "count": participants.count()}

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

    # def validate_phone_number(self, phone_number, country=None):
    #     if country == None or country == "Kenya":
    #         reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
    #         reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
    #         reg2 = re.compile(r"^[0]\d{9}$")
    #         reg3 = re.compile(r"^[7]\d{8}$")
    #         phone_number = re.sub(r"\s+", "", phone_number)
    #         if reg.search(phone_number):
    #             return phone_number
    #         elif reg1.search(phone_number):
    #             phone_number = phone_number.replace("+", "")
    #             return phone_number
    #         elif reg2.search(phone_number):
    #             phone_number = re.sub(phone_number[0], "254", phone_number, 1)
    #             return phone_number
    #         elif reg3.search(phone_number):
    #             phone_number = "254" + phone_number[:9]
    #             return phone_number
    #         else:
    #             return False
    #     else:
    #         HC = Helpcontacts.objects.get(country=country)
    #         calling_code = HC.country_calling_code
    #         reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
    #         reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
    #         reg2 = re.compile(r"^[0]\d{9}$")
    #         reg3 = re.compile(r"^[7]\d{8}$")
    #         phone_number = re.sub(r"\s+", "", phone_number)
    #         try:
    #             if reg.search(phone_number):
    #                 return phone_number
    #             elif reg1.search(phone_number):
    #                 phone_number = phone_number.replace("+", "")
    #                 return phone_number
    #             elif reg2.search(phone_number):
    #                 phone_number = re.sub(
    #                     phone_number[0], calling_code, phone_number, 1
    #                 )
    #                 return phone_number
    #             elif reg3.search(phone_number):
    #                 phone_number = calling_code + phone_number[:9]
    #                 return phone_number
    #             else:
    #                 return False
    #         except Exception as e:
    #             capture_exception(e)

    # def invite_suppliers_sms(self, supplier_phone_number, count, country=None):
    #     api_url = "http://52.15.88.116/bulkAPIV2/"
    #     valid_phone_number = self.validate_phone_number(supplier_phone_number, country)
    #     if valid_phone_number:
    #         try:
    #             request_sms = {
    #                 "user": settings.MTECH_API_USER,
    #                 "pass": settings.MTECH_API_PASS,
    #                 "message": f"Tendersure is managing the prequalification for {self.job.company}.Closing date {self.closing_date.date()}.To bid go to www.tendersure.co.ke and click 'Available Jobs'",
    #                 "msisdn": valid_phone_number,
    #                 "shortCode": settings.MTECH_API_SHORTCODE,
    #                 "messageID": f"{ self.name }" + f"{ count }",
    #                 "coding": "utf-8",
    #             }
    #             response = requests.get(api_url, params=request_sms)
    #         except Exception as e:
    #             capture_exception(e)

    # def invite_suppliers(self):
    #     countries = ["Uganda", "Malawi", "Zambia", "Mozambique"]
    #     country = self.job.company.country
    #     if self.invite_notification == False:
    #         count = 0
    #         suppliers = self.category_type.suppliers_list(
    #             country=self.job.company.country
    #         )
    #         old_suppliers = suppliers["old_suppliers"]
    #         registered_suppliers = suppliers["registered_suppliers"]
    #
    #         # for registered  suppliers
    #         for registered_supplier in registered_suppliers:
    #             if registered_supplier.phone_number != "":
    #                 if country not in countries:
    #                     self.invite_suppliers_sms(
    #                         registered_supplier.phone_number, count
    #                     )
    #                     count += 1
    #                 else:
    #                     self.invite_suppliers_sms(
    #                         registered_supplier.phone_number, count, country
    #                     )
    #                     count += 1
    #             else:
    #                 continue
    #
    #         # for old suppliers
    #         for old_supplier in old_suppliers:
    #             if old_supplier.primary_phone != "":
    #                 if country not in countries:
    #                     self.invite_suppliers_sms(old_supplier.primary_phone, count)
    #                     count += 1
    #                 else:
    #                     self.invite_suppliers_sms(
    #                         old_supplier.primary_phone, count, country
    #                     )
    #                     count += 1
    #             else:
    #                 continue
    #
    #         self.invite_notification = True
    #         self.save()
    #         return suppliers
    #     return False

    # def invite_suppliers_emails(self):
    #     countries = ["Uganda", "Malawi", "Zambia", "Tanzania", "Mozambique"]
    #     if self.invite_notification == False:
    #         if self.invite_only == True:
    #             """
    #             Send notifications for closed prequal
    #             """
    #             pass
    #
    #         else:
    #             """
    #             Send notifications for open prequal
    #             """
    #             suppliers = self.category_type.suppliers_list_emails(
    #                 country=self.job.company.country
    #             )
    #             buyer = Buyer.objects.filter(company=self.job.company).first()
    #             country = self.job.company.country
    #             old_suppliers = list(suppliers["old_suppliers"])
    #             registered_suppliers = suppliers["registered_suppliers"]
    #             supplier_emails = old_suppliers.extend(registered_suppliers)
    #             # for loop  was here
    #             if len(old_suppliers) >= 99:
    #                 no_of_suppliers = len(old_suppliers)
    #                 no_of_lists = no_of_suppliers // 99
    #                 if no_of_suppliers % 99 != 0:
    #                     no_of_lists += 1
    #                 split_old_suppliers = np.array_split(old_suppliers, no_of_lists)
    #
    #                 count = 1
    #                 for split_old_supplier in split_old_suppliers:
    #                     split_old_supplier = list(split_old_supplier)
    #
    #                     # half = len(old_suppliers)//2
    #                     # second_half = old_suppliers[:half]
    #                     # old_suppliers = old_suppliers[half:]
    #                     if country not in countries:
    #                         try:
    #                             body = render_to_string(
    #                                 "supplier_portal/emails/supplier_invite.html",
    #                                 {
    #                                     "supplier": "Esteemed Vendor",
    #                                     "company": self.job.company,
    #                                     "category": self.name,
    #                                 },
    #                             )
    #
    #                             message = render_to_string(
    #                                 "supplier_portal/emails/supplier_invite.html",
    #                                 {
    #                                     "supplier": "Esteemed Vendor",
    #                                     "company": self.job.company,
    #                                     "category": self.name,
    #                                 },
    #                             )
    #                             email_subject = f"{self.job.job_title.upper()} NOTICE"
    #
    #                             A = PrivateMediaStorage()
    #                             headers = {"ResponseContentDisposition": f"attachment;"}
    #                             time = datetime.datetime.now()
    #                             file_url = A.url(
    #                                 f"{self.job.advert}",
    #                                 expire=300,
    #                                 parameters=headers,
    #                                 http_method="GET",
    #                             )
    #                             dir_name = Path(
    #                                 "media/temp/{}/{}/{}".format(
    #                                     time.year, time.month, time.day
    #                                 )
    #                             )  # folder structure
    #                             dir_name.mkdir(parents=True, exist_ok=True)
    #                             file_name = os.path.basename(f"{self.job.advert}")
    #                             filepath = "{}/{}".format(dir_name, file_name)
    #                             r = requests.get(file_url)
    #                             with open("{}".format(filepath), "wb") as f:
    #                                 f.write(r.content)
    #
    #                             email = EmailMultiAlternatives(
    #                                 subject=email_subject,
    #                                 body=body,
    #                                 from_email=default_from_email_sendinblue,
    #                                 bcc=split_old_supplier,
    #                                 connection=connection,
    #                             )
    #                             email.attach_alternative(message, "text/html")
    #                             email.attach_file(filepath)
    #                             email.send(fail_silently=True)
    #                             try:
    #                                 for supplier_email in split_old_supplier:
    #                                     if Supplier.objects.filter(
    #                                         email=supplier_email
    #                                     ).exists():
    #                                         save_supplier_buyer_emails(
    #                                             supplier_email=supplier_email,
    #                                             buyer_id=buyer.id,
    #                                             job_id=self.job.id,
    #                                             email_subject=email_subject,
    #                                             email_body=body,
    #                                         )
    #                             except Exception as e:
    #                                 capture_exception(e)
    #
    #                             # print(f'Sending second half')
    #                             # self.sending_second_half(second_half, country)
    #                         except Exception as e:
    #                             capture_exception(e)
    #                             # print(f'Sending second half')
    #                             # self.sending_second_half(second_half, country)
    #
    #                         self.invite_notification = True
    #                         self.save()
    #                         count += 1
    #                     else:
    #                         # send with  personalized phone and email
    #                         help_contacts = Helpcontacts.objects.get(country=country)
    #                         try:
    #                             body = render_to_string(
    #                                 "supplier_portal/emails/custom_emails/supplier_invite.html",
    #                                 {
    #                                     "supplier": "Esteemed Vendor",
    #                                     "company": self.job.company,
    #                                     "category": self.name,
    #                                     "phone": help_contacts.contact_phone,
    #                                     "help_email": help_contacts.helpemail,
    #                                 },
    #                             )
    #
    #                             message = render_to_string(
    #                                 "supplier_portal/emails/custom_emails/supplier_invite.html",
    #                                 {
    #                                     "supplier": "Esteemed Vendor",
    #                                     "company": self.job.company,
    #                                     "category": self.name,
    #                                     "phone": help_contacts.contact_phone,
    #                                     "help_email": help_contacts.helpemail,
    #                                 },
    #                             )
    #                             email_subject = f"{self.job.job_title.upper()} NOTICE"
    #
    #                             A = PrivateMediaStorage()
    #                             headers = {"ResponseContentDisposition": f"attachment;"}
    #                             time = datetime.datetime.now()
    #                             file_url = A.url(
    #                                 f"{self.job.advert}",
    #                                 expire=300,
    #                                 parameters=headers,
    #                                 http_method="GET",
    #                             )
    #                             dir_name = Path(
    #                                 "media/temp/{}/{}/{}".format(
    #                                     time.year, time.month, time.day
    #                                 )
    #                             )  # folder structure
    #                             dir_name.mkdir(parents=True, exist_ok=True)
    #                             file_name = os.path.basename(f"{self.job.advert}")
    #                             filepath = "{}/{}".format(dir_name, file_name)
    #                             r = requests.get(file_url)
    #                             with open("{}".format(filepath), "wb") as f:
    #                                 f.write(r.content)
    #
    #                             email = EmailMultiAlternatives(
    #                                 subject=email_subject,
    #                                 body=body,
    #                                 bcc=split_old_supplier,
    #                                 from_email=default_from_email_sendinblue,
    #                                 connection=connection,
    #                             )
    #                             email.attach_alternative(message, "text/html")
    #                             email.attach_file(filepath)
    #                             email.send(fail_silently=True)
    #                             # print(f'Sending second half')
    #                             # self.sending_second_half(second_half, country)
    #                         except Exception as e:
    #                             capture_exception(e)
    #                             # print(f'Sending second half')
    #                             # self.sending_second_half(second_half, country)
    #                         self.invite_notification = True
    #                         self.save()
    #                 return True
    #             else:
    #                 if country not in countries:
    #                     try:
    #                         body = render_to_string(
    #                             "supplier_portal/emails/supplier_invite.html",
    #                             {
    #                                 "supplier": "Esteemed Vendor",
    #                                 "company": self.job.company,
    #                                 "category": self.name,
    #                             },
    #                         )
    #
    #                         message = render_to_string(
    #                             "supplier_portal/emails/supplier_invite.html",
    #                             {
    #                                 "supplier": "Esteemed Vendor",
    #                                 "company": self.job.company,
    #                                 "category": self.name,
    #                             },
    #                         )
    #                         email_subject = f"{self.job.job_title.upper()} NOTICE"
    #
    #                         A = PrivateMediaStorage()
    #                         headers = {"ResponseContentDisposition": f"attachment;"}
    #                         time = datetime.datetime.now()
    #                         file_url = A.url(
    #                             f"{self.job.advert}",
    #                             expire=300,
    #                             parameters=headers,
    #                             http_method="GET",
    #                         )
    #                         dir_name = Path(
    #                             "media/temp/{}/{}/{}".format(
    #                                 time.year, time.month, time.day
    #                             )
    #                         )  # folder structure
    #                         dir_name.mkdir(parents=True, exist_ok=True)
    #                         file_name = os.path.basename(f"{self.job.advert}")
    #                         filepath = "{}/{}".format(dir_name, file_name)
    #                         r = requests.get(file_url)
    #                         with open("{}".format(filepath), "wb") as f:
    #                             f.write(r.content)
    #
    #                         email = EmailMultiAlternatives(
    #                             subject=email_subject,
    #                             body=body,
    #                             from_email=default_from_email_sendinblue,
    #                             bcc=old_suppliers,
    #                             connection=connection,
    #                         )
    #
    #                         email.attach_alternative(message, "text/html")
    #                         email.attach_file(filepath)
    #                         email.send(fail_silently=True)
    #                         connection.close()
    #                     except Exception as e:
    #                         capture_exception(e)
    #
    #                     self.invite_notification = True
    #                     self.save()
    #                     return old_suppliers
    #                 else:
    #                     # send with  personalized phone and email
    #                     help_contacts = Helpcontacts.objects.get(country=country)
    #                     try:
    #                         body = render_to_string(
    #                             "supplier_portal/emails/custom_emails/supplier_invite.html",
    #                             {
    #                                 "supplier": "Esteemed Vendor",
    #                                 "company": self.job.company,
    #                                 "category": self.name,
    #                                 "phone": help_contacts.contact_phone,
    #                                 "help_email": help_contacts.helpemail,
    #                             },
    #                         )
    #
    #                         message = render_to_string(
    #                             "supplier_portal/emails/custom_emails/supplier_invite.html",
    #                             {
    #                                 "supplier": "Esteemed Vendor",
    #                                 "company": self.job.company,
    #                                 "category": self.name,
    #                                 "phone": help_contacts.contact_phone,
    #                                 "help_email": help_contacts.helpemail,
    #                             },
    #                         )
    #                         email_subject = f"{self.job.job_title.upper()} NOTICE"
    #
    #                         A = PrivateMediaStorage()
    #                         headers = {"ResponseContentDisposition": f"attachment;"}
    #                         time = datetime.datetime.now()
    #                         file_url = A.url(
    #                             f"{self.job.advert}",
    #                             expire=300,
    #                             parameters=headers,
    #                             http_method="GET",
    #                         )
    #                         dir_name = Path(
    #                             "media/temp/{}/{}/{}".format(
    #                                 time.year, time.month, time.day
    #                             )
    #                         )  # folder structure
    #                         dir_name.mkdir(parents=True, exist_ok=True)
    #                         file_name = os.path.basename(f"{self.job.advert}")
    #                         filepath = "{}/{}".format(dir_name, file_name)
    #                         r = requests.get(file_url)
    #                         with open("{}".format(filepath), "wb") as f:
    #                             f.write(r.content)
    #
    #                         email = EmailMultiAlternatives(
    #                             subject=email_subject,
    #                             body=body,
    #                             bcc=old_suppliers,
    #                             from_email=default_from_email_sendinblue,
    #                             connection=connection,
    #                         )
    #                         email.attach_alternative(message, "text/html")
    #                         email.attach_file(filepath)
    #                         email.send(fail_silently=True)
    #                         connection.close()
    #                     except Exception as e:
    #                         capture_exception(e)
    #
    #                     self.invite_notification = True
    #                     self.save()
    #                     return old_suppliers
    #     return False


class Section(BaseModel):
    name = models.CharField(max_length=200, db_index=True)
    trans_name = models.CharField(max_length=200, blank=True, null=True)
    short_name = models.CharField(max_length=100, blank=True, null=True)
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
        return self.name

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
    def section_score(self):
        questions = Question.objects.filter(section_id=self.id, is_scored=True).annotate(section_score=Sum('max_score'))
        if questions:
            return questions.first().section_score
        return 0

    @property
    def questions(self):
        return Question.objects.filter(section_id=self.id)

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
    description = models.TextField()
    trans_description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    trans_short_description = models.TextField(blank=True, null=True)
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

    @property
    def marking_scheme(self):
        if MarkingScheme.objects.filter(question=self).count() > 0:
            return MarkingScheme.objects.filter(question=self).first()
        return None


class MarkingScheme(BaseModel):
    question = models.ForeignKey(
        Question, blank=False, null=False, on_delete=models.CASCADE
    )
    options = models.TextField(default="", db_index=True)
    # options = models.TextField(blank=True, null=True, default="")
    score = models.TextField(default="", db_index=True)

    class Meta:
        verbose_name = "Marking Scheme"
        verbose_name_plural = "Marking Schemes"


class SupplierResponse(BaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier,
        related_name="tender_supplier_response", on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to=supplier_response_files, validators=validators,
        blank=True, null=True, max_length=1000,
        storage=PrivateMediaStorage()
    )
    options = pgcrypto.EncryptedTextField(
        max_length=100000, db_index=True, blank=True, null=True
    )

    class Meta:
        verbose_name = "Supplier Response"
        verbose_name_plural = "Supplier Responses"

    @property
    def full_document_url(self):
        response = None
        if self.document_url:
            response = get_document_url(f"{self.document_url}")
        return response

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
        Supplier, on_delete=models.CASCADE, related_name="qa_response_supplier"
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
        User, blank=False, related_name="qa_response_created_by",
        null=True, on_delete=models.CASCADE,
    )
    verified_by = models.ForeignKey(
        User, blank=True, related_name="qa_response_verified_by",
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
        User, blank=True, null=True, on_delete=models.CASCADE, related_name="dd_created_by"
    )

    class Meta:
        verbose_name = "Due Diligence"
        verbose_name_plural = "Due Diligence"

    def __str__(self):
        return self.category.name


class DueDiligenceSupplier(BaseModel):
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="dd_supplier"
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
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="section_score_supplier"
    )
    score = models.BigIntegerField()
    score_after_qa = models.BigIntegerField(null=True, blank=True)


# class PrequalReport(BaseModel):
#     tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
#     bidder_information = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     technical_evaluation = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     technical_evaluation_summary = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     technical_evaluation_responses = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     qa_ranking_pdf = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     qa_ranking_excel = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     qa = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#     dd = models.FileField(
#         upload_to="prequal/reports/%Y/%m/%d", validators=validators,
#         storage=PrivateMediaStorage(), blank=True, null=True,
#     )
#
#     class Meta:
#         verbose_name = "Prequal Report"
#         verbose_name_plural = "Prequal Reports"


# models related to letters
class AwardLetter(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="award_letter_supplier"
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
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="tender_payment_supplier"
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
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="regret_letter_supplier"
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
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="dd_letter_supplier"
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
        Supplier, blank=False, null=False, on_delete=models.CASCADE, related_name="custom_letter_supplier"
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


class Item(BaseModel):
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
    description = models.TextField(db_index=True)
    unit_of_measure = models.TextField()
    number = models.IntegerField(db_index=True)
    current_price = models.TextField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=1, db_index=True)
    outlier_score_final = models.FloatField(null=True, blank=True)
    upper_outlier_score_final = models.FloatField(null=True, blank=True)
    median_price_final = models.FloatField(null=True, blank=True)
    savings_value = models.FloatField(null=True, blank=True)
    eprocure_total_value = models.FloatField(null=True, blank=True)
    code = models.CharField(max_length=100, blank=True, null=True)
    price_validity_months = models.IntegerField(null=True, blank=True)
    specification_1 = models.TextField(blank=True, null=True)
    specification_2 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Tender Item"
        verbose_name_plural = "Tender Items"
        ordering = ["-id"]

    def eprocure_suppliers(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.is_open:
            if responses is None:
                responses = self.responses
            suppliers = []
            for response in responses:
                if response.total is not None:
                    try:
                        response_total = show(response.total)
                    except:
                        response_total = 0
                else:
                    response_total = 0
                if (
                    float(self.outlier_score)
                    < response_total
                    < float(self.upper_outlier_score)
                ):
                    # eliminate outliers and non responsives
                    suppliers.append(
                        {
                            "supplier": response.supplier.supplier_name.title(),
                            "price": response_total,
                        }
                    )
            sorted_suppliers = sorted(suppliers, key=lambda i: i["price"])
            tendersure_suppliers = sorted_suppliers[:3]
            # tendersure_suppliers = [o['supplier'] for o in tendersure_suppliers]
            if len(tendersure_suppliers) == 2:
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
            elif len(tendersure_suppliers) == 1:
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
            elif len(tendersure_suppliers) == 0:
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
                tendersure_suppliers.append({"supplier": "N/A", "price": "N/A"})
            else:
                pass

            # print(tendersure_suppliers)

            return tendersure_suppliers

        return ["", "", ""]


    @property
    def responses(self):
        return ItemResponse.objects.filter(item_id=self.id)

    @property
    def outlier_score(self):
        outlier_score = 0.50 * self.median_price
        self.outlier_score_final = outlier_score
        self.save()
        return outlier_score

    @property
    def current_total(self):
        # get the item current total cost
        return round(float(self.current_price))

    def savings(self, responses=None):
        if self.current_total == 0:
            return 0
        if responses is None:
            responses = self.responses
        saving = self.current_total - self.eprocure_total(responses)
        if saving < 0:
            saving = 0
        return saving

    def percentage_savings(self, responses=None):
        if self.current_total == 0:
            return "0%"
        if responses is None:
            responses = self.responses

        result = "{}%".format(
            round((self.savings(responses) / self.current_total) * 100)
        )
        return result

    @property
    def median_price(self):
        """Get the median reference point for purpose of eliminating outliers"""
        prices = []
        for response in self.responses:
            if response.total is not None:
                bid_price = float(show(response.total))
                if bid_price > 0:
                    prices.append(bid_price)
            else:
                bid_price = 0

        median = 0
        if len(prices) > 0:
            median = statistics.median(prices)
        self.median_price_final = median
        self.save()
        return median

    @property
    def upper_outlier_score(self):
        upper_outlier_score = 1.75 * self.median_price
        self.upper_outlier_score_final = upper_outlier_score
        self.save()
        return upper_outlier_score

    def eprocure_total(self, responses=None):
        if responses is None:
            responses = self.responses
        return round(self.eprocure_supplier_cost(responses), 2)

    def eprocure_supplier_cost(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.is_open:
            cheapest = 99999999999999999.9  # to reduce processing time to O(1)
            if responses is None:
                responses = self.responses
            for response in responses:
                if response.value is not None:
                    response_total = response.value
                    # try:
                    #     response_total = show(response.total)
                    # except:
                    #     response_total = 0
                else:
                    response_total = 0
                if (
                    float(self.outlier_score) < response_total < cheapest
                ):  # eliminate outliers and non responsives
                    cheapest = response_total
            if cheapest != 99999999999999999.9:
                return round(cheapest, 2)
        return 0

    def multi_item_tender_eprocure_suppliers_with_tt_tech_weight(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.is_open:
            if responses is None:
                responses = self.responses
            responses = responses.order_by("value")
            lowest = responses.first()
            suppliers = []
            for response in responses:

                if response.total is not None:
                    response_total = show(response.total)
                else:
                    response_total = 0

                weighted_score = response.supplier.tender_total_item_weighted_score(
                    item=response.item)
                if responses.count() <= 2:
                    suppliers.append(
                        {
                            "supplier": response.supplier.short_name.title(),
                            "price": response_total, "weighted_score": f"Tc_{weighted_score}",
                        }
                    )
                else:
                    if float(self.outlier_score) < response_total:
                        suppliers.append(
                            {
                                "supplier": response.supplier.short_name.title(),
                                "price": response_total, "weighted_score": f"Tc_{weighted_score}",
                            }
                        )

            sorted_suppliers = sorted(
                suppliers, key=lambda i: i["weighted_score"], reverse=True
            )
            tendersure_suppliers = sorted_suppliers[:5]
            if len(tendersure_suppliers) == 4:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 3:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 2:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 1:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 0:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            else:
                pass
            return tendersure_suppliers
        return ["", "", ""]

    def multi_item_tender_eprocure_suppliers(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.is_open:
            if responses is None:
                responses = self.responses
            responses = responses.order_by("value")
            lowest = responses.first()
            suppliers = []
            for response in responses:
                if response.total_price is not None:
                    response_total = response.total_price
                else:
                    response_total = 0

                if responses.count() <= 2:
                    suppliers.append(
                        {
                            "supplier": response.supplier.company_name.title(),
                            "price": response_total,
                            "weighted_score": 0,
                        }
                    )
                else:
                    # if float(self.outlier_score) < response_total < float(self.upper_outlier_score):
                    if float(self.outlier_score) < response_total:
                        suppliers.append(
                            {
                                "supplier": response.supplier.company_name.title(),
                                "price": response_total,
                                "weighted_score": 0,
                            }
                        )

            sorted_suppliers = sorted(suppliers, key=lambda i: i["price"])
            tendersure_suppliers = sorted_suppliers[:5]
            if len(tendersure_suppliers) == 4:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 3:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 2:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 1:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            elif len(tendersure_suppliers) == 0:
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
                tendersure_suppliers.append(
                    {"supplier": "N/A", "price": "N/A", "weighted_score": "N/A"}
                )
            else:
                pass
            return tendersure_suppliers
        return ["", "", ""]

class SupplierFinancialResponse(BaseModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=True, on_delete=models.CASCADE, related_name="fr_supplier"
    )
    category = models.ForeignKey(Category, blank=False, null=True, on_delete=models.CASCADE)
    awarded = models.BooleanField(default=False)
    excel_url = models.FileField(
       upload_to="Rfq/%Y/%m/%d",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Supplier Financial Response"
        verbose_name_plural = "Supplier Financial Responses"

    def __str__(self):
        return self.supplier.username

    @property
    def full_document_url(self):
        response = None
        if self.excel_url:
            response = get_document_url(f"{self.excel_url}")
        return response


class ItemResponse(BaseModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=True, on_delete=models.CASCADE, related_name="item_response_supplier"
    )
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE)
    total = models.TextField(null=True)
    cell_data = models.TextField(null=True, db_index=True)  # save json
    column_data = models.TextField(null=True, db_index=True)  # save Json
    item_number = models.IntegerField(db_index=True)  # the item number in the excel
    value = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    unit_price = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Item Response"
        verbose_name_plural = "Item Responses"


class SupplierTechnicalScore(BaseModel):
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(
        Supplier, blank=False, null=False, on_delete=models.CASCADE,
        related_name="category_score_supplier"
    )
    score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    weighted_score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    score_after_qa = models.DecimalField(max_digits=20, decimal_places=6, null=True, blank=True)
    rank = models.BigIntegerField(default=0)
    rank_after_qa = models.BigIntegerField(null=True, blank=True)
    technically_qualified = models.BooleanField(default=True)
    meets_all_mandatory_requirements = models.BooleanField(null=True, default=True)

    class Meta:
        verbose_name = "Supplier Technical Score"
        verbose_name_plural = "Supplier Technical Scores"


class SupplierFinancialTotal(BaseModel):
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    has_outlier = models.BooleanField(default=False)
    has_blank = models.BooleanField(default=False, null=True, blank=True)
    score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    rank = models.BigIntegerField(default=0)
    technically_qualified = models.BooleanField(default=True)
    meets_all_mandatory_requirements = models.BooleanField(null=True, default=True)
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=False, on_delete=models.CASCADE, related_name="rfq_total_supplier"
    )

    class Meta:
        verbose_name = "Supplier Financial Total"
        verbose_name_plural = "Supplier Financial Totals"


class SupplierCategoryScore(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(Supplier, blank=False, related_name='tender_category_supplier', null=False, on_delete=models.CASCADE)
    technical_score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    financial_score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    has_outlier = models.BooleanField(default=False)
    has_blank = models.BooleanField(default=False, null=True, blank=True)
    technically_qualified = models.BooleanField(default=True)
    meets_all_mandatory_requirements = models.BooleanField(null=True, default=True)
    rank = models.BigIntegerField(db_index=True, default=0)

    class Meta:
        verbose_name = "Supplier Category Score"
        verbose_name_plural = "Supplier Category Scores"


class Invitee(BaseModel):
    category = models.ForeignKey(Category, blank=False, null=False, on_delete=models.CASCADE)
    email = models.EmailField()
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=True, null=True, on_delete=models.CASCADE, related_name="tc_invitee"
    )

    class Meta:
        verbose_name = "Category Invitee"
        verbose_name_plural = "Category Invitees"


class JobReport(BaseModel):
    tender = models.ForeignKey(Tender, on_delete=models.CASCADE)
    interim_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    qa_ranking_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    bidder_locations_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    prequalified_suppliers_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    bidder_payments_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    responsive_bidders_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    non_responsive_bidders_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    directors_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    participation_status_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    dd_ranking_report = models.FileField(
        upload_to="tender/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    supplier_details_report = models.FileField(
            upload_to="tender/job/reports", validators=validators, blank=True,
            null=True, max_length=3000,
            storage=PrivateMediaStorage()
        )
    category_suppliers_report = models.FileField(
            upload_to="tender/job/reports", validators=validators, blank=True,
            null=True, max_length=3000,
            storage=PrivateMediaStorage()
        )

    class Meta:
        verbose_name = "Job Report"
        verbose_name_plural = "Job Reports"


class CategoryReport(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    bidder_information = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        blank=True, null=True,
        storage=PrivateMediaStorage()
    )
    technical_evaluation_summary = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    technical_evaluation_responses = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_pdf = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa_ranking_excel = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    qa = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    dd = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )
    consolidated_tender_summary_report = models.FileField(
        upload_to="tender/category/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    multi_item_tender_summary_report = models.FileField(
        upload_to="tender/category/job/reports", validators=validators, blank=True,
        null=True, max_length=3000,
        storage=PrivateMediaStorage()
    )
    financial_ratios = models.FileField(
        upload_to="tender/category/reports/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
    )

    class Meta:
        verbose_name = "Tender Report"
        verbose_name_plural = "Tender Reports"


class SupplierPDFResponse(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier,
        related_name="tender_supplier_pdf_response",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    document_url = models.FileField(
        upload_to="tender/supplier_pdf_responses",
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
        # storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
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


class FinancialRatio(BaseModel):
    supplier = models.ForeignKey(Supplier, related_name='tender_financial_supplier', on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    equity = models.DecimalField(max_digits=15, decimal_places=2, null=True)
    curr_liabilities = models.DecimalField(help_text="Current Liabilities", max_digits=15, decimal_places=2, blank=True,null=True)
    fixed_assets = models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
    current_assets= models.DecimalField(max_digits=15, decimal_places=2,blank=True, null=True)
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
        related_name="question_archive",
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
    tender = models.ForeignKey(
        Tender, blank=True, null=True, on_delete=models.CASCADE)
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
