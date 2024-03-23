from operator import mod
from pyexpat import model
from tabnanny import verbose
import time

from django.apps import apps
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template.loader import render_to_string
from apps.common.utils import timezone_aware_time

from apps.core.models import BaseModel, CategoryType, Currency
from apps.core.utils import show, get_document_url
from backend import settings
from pathlib import Path
import requests
import datetime
import os
from backend.storage_backends import PrivateMediaStorage
from django.core.validators import FileExtensionValidator
import statistics

# from ..companyManagment.models import CompanyUser


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


class Rfq(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("final", "Published"),
    )

    company = models.ForeignKey("buyer.Company", on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    approved_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rfq_approved_by", null=True
    )
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="rfq_created_by"
    )
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="draft")
    old_system = models.BooleanField(default=False)
    show_bids = models.BooleanField(default=False)
    lang_en = models.BooleanField(default=False)
    advert = models.FileField(
        upload_to="job/advert",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=3000,
    )
    current_suppliers = models.FileField(
        upload_to="job/current_suppliers", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=3000)
    category_suppliers = models.FileField(
        upload_to="job/current_suppliers", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=3000)
    bidding_instructions = models.FileField(
        upload_to="job/bidding_instructions",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=3000,
    )

    class Meta:
        verbose_name = "RFQ Job"
        verbose_name_plural = "RFQ Jobs"
        ordering = ["-id"]
    
    @property
    def closed_rfqs(self):
        return Category.objects.filter(rfq=self, status_open=False).order_by("unique_reference")


    @property
    def categories(self):
        return Category.objects.filter(rfq=self).order_by("unique_reference")


class Category(BaseModel):
    RFQ_TYPE_CHOICES = (
        ("basic", "Basic"),
        ("advanced", "Advanced"),
    )

    rfq = models.ForeignKey(Rfq, on_delete=models.CASCADE)
    category_type = models.ForeignKey(
        CategoryType, on_delete=models.CASCADE, related_name="rfqs"
    )
    name = models.CharField(max_length=1000, db_index=True)
    opening_date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    closing_date = models.DateTimeField(db_index=True, default=datetime.datetime.now)
    evaluation_date = models.DateTimeField(db_index=True, null=True, blank=True)
    unique_reference = models.TextField(unique=True)
    status_open = models.BooleanField(default=False)
    invite_notification = models.BooleanField(default=False)
    instructions = models.TextField()
    self_evaluate = models.BooleanField(default=True)
    total_savings = models.FloatField(default=0, null=True, blank=True)
    total_column = models.CharField(max_length=250, default="TOTAL")
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE, related_name="rfq_currency"
    )
    rfq_type = models.CharField(choices=RFQ_TYPE_CHOICES, max_length=10, default="basic")
    vatable = models.BooleanField(default=True)
    vat_rate = models.FloatField(default=16.0, null=True, blank=True)
    report = models.FileField(
        upload_to="Rfq/reports/%Y/%m/%d", validators=validators,
        blank=True, null=True, max_length=1000, storage=PrivateMediaStorage()
    )
    published = models.BooleanField(default=False)
    items_template = models.FileField(
        upload_to="Rfq/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True,
        max_length=1000)
    current_prices_template = models.FileField(
        upload_to="Rfq/current_prices/%Y/%m/%d", validators=validators,
        blank=True, null=True,max_length=2000, storage=PrivateMediaStorage())

    class Meta:
        verbose_name = "Request for Quotation"
        verbose_name_plural = "Requests for Quotations"

    def __str__(self):
        return "(%s) %s" % (self.unique_reference, self.name)

    @property
    def items(self):
        return RFQItem.objects.filter(category_id=self.id).order_by("item_number")

    @property
    def items_count(self):
        return RFQItem.objects.filter(category_id=self.id).count()

    @property
    def invited_suppliers(self):
        suppliers = []
        invitees = RfqInvitee.objects.filter(category=self)
        for invitation in invitees:
            if invitation.supplier is None:
                sup = invitation.email
            else:
                sup = invitation.supplier
            suppliers.append(sup)
        return list(set(suppliers))

    def refresh_scores(self):
        try:
            items = RFQItem.objects.filter(rfq_id=self.id)
            for item in items:
                item.outlier_score_final = None
                item.upper_outlier_score_final = None
                item.median_price_final = None
                item.save()

            suppliers = apps.get_model("suppliers", "Supplier").objects.filter(
                id__in=SupplierResponse.objects.filter(rfq_id=self.id)
                .only("supplier_id")
                .values("supplier_id")
            )

            lowest_price = 100000000000000000
            for supplier in suppliers:
                # resolve_rfq_score(supplier_id=supplier.id, rfq=self)
                pass
            self.rank_participants()
        except Exception as e:
            print(e)

    def rank_participants(self):
        try:
            scores = SupplierRfqTotal.objects.filter(
                category_id=self.id, has_outlier=False
            ).order_by("-score")
            rank = 0
            if scores.count() == 0:
                return True

            first_score = scores.first()
            first_score.rank = 1
            first_score.save()
            prev_score = first_score
            for rfq_score in scores:
                if rfq_score.score == prev_score.score:
                    rfq_score.rank = prev_score.rank
                else:
                    rfq_score.rank = rank + 1

                if rfq_score.has_outlier:
                    rfq_score.rank = 0
                rank += 1
                rfq_score.save()
                prev_score = rfq_score
        except Exception as e:
            print(e)

    def relative_report_url(self):
        if self.report is not None:
            excel_path = "{}".format(self.report)
            A = PrivateMediaStorage()
            headers = {"ResponseContentDisposition": f"attachment;"}
            time = datetime.datetime.now()
            file_url = A.url(
                f"{excel_path}", expire=300, parameters=headers, http_method="GET"
            )
            dir_name = Path(
                "media/temp/{}/{}/{}".format(time.year, time.month, time.day)
            )  # folder structure
            dir_name.mkdir(parents=True, exist_ok=True)
            file_name = os.path.basename(f"{excel_path}")
            filepath = "{}/{}".format(dir_name, file_name)
            my_file = Path(filepath)
            if my_file.is_file():
                # print(f"{filepath} exists")
                return filepath
            r = requests.get(file_url)
            with open("{}".format(filepath), "wb") as f:
                f.write(r.content)

            return filepath
        return None

    @property
    def participants(self):
        suppliers = []
        rfq_scores = SupplierRfqTotal.objects.filter(category_id=self.id).values_list(
            "supplier_id", flat=True
        )
        if rfq_scores.count() == 0:
            responses = RFQItemResponse.objects.filter(
                rfq_item__category_id=self.id
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
                id__in=rfq_scores
            )
            return {"participants": participants, "count": len(participants)}

    def rfq_sorted_participants(self, participants=None):
        sorted_participants = []
        first_score = SupplierRfqTotal.objects.filter(rfq_id=self.id).first()
        if first_score is None:
            # get a first score by calculating rfq scores for each participant
            if participants is None:
                participants = self.participants
            for participant in participants:
                participant.resolve_rfq_score(self)
            first_score = SupplierRfqTotal.objects.filter(rfq_id=self.id).first()
            if first_score is not None:
                if first_score.rank is None or first_score.rank == 0:
                    self.rank_participants()
        else:
            if first_score.rank is None or first_score.rank == 0:
                self.rank_participants()

        scores = SupplierRfqTotal.objects.filter(rfq_id=self.id).extra(
            select={
                "not_ranked": "rank = 0",
            },
            order_by=["not_ranked", "rank"],
        )

        for score in scores:
            sorted_participants.append(score.supplier)

        return sorted_participants

    def items_current_cost(self, items=None):
        current_cost = 0
        if items is None:
            items = self.items
        for item in items:
            current_cost += item.current_total
        return current_cost

    def total_current_cost(self, items=None):
        current_cost = 0
        if items is None:
            items = self.items
        for item in items:
            cost = item.current_total * item.quantity
            current_cost += cost
        return current_cost

    def total_potential_savings(self, items=None):
        potential_savings = 0
        if items is None:
            items = self.items
        for item in items:
            responses = item.responses
            savings = item.savings(responses) * item.quantity
            potential_savings += savings
        if potential_savings < 0:
            potential_savings = 0
        return round(potential_savings, 2)

    def items_potential_savings(self, items=None):
        potential_savings = 0
        if items is None:
            items = self.items
        for item in items:
            responses = item.responses
            potential_savings += item.savings(responses)
        if potential_savings < 0:
            potential_savings = 0
        return round(potential_savings, 2)

    def eprocure_total_cost(self, items=None):
        eprocure_cost = 0
        if items is None:
            items = self.items
        for item in items:
            responses = item.responses
            eprocure_cost += item.eprocure_total(responses)
        return eprocure_cost

    def lowest_cost(self, items=None):
        rfq_lowest_cost = 0
        if items is None:
            items = self.items
            for item in items:
                responses = item.responses
                lowest_cost = item.eprocure_supplier_cost(responses)
                rfq_lowest_cost += lowest_cost

        return rfq_lowest_cost

    def current_cost(self, items=None):
        if not self.status_open:
            if items is None:
                items = RFQItem.objects.filter(rfq_id=self.id)
            current_sum = 0
            for item in items:
                current_sum += float(item.current_price)
            return round(current_sum, 2)
        return 0

    def eprocure_cost(self, items=None):
        if not self.status_open:  # the job must be closed to show these values
            if items is None:
                items = RFQItem.objects.filter(rfq=self)
            eprocure_cost = 0
            for item in items:
                responses = item.responses
                eprocure_cost += item.eprocure_supplier_cost(responses)
            return round(eprocure_cost, 2)
        return 0


class RFQItem(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=True, on_delete=models.CASCADE
    )
    item_description = models.TextField(db_index=True)
    item_number = models.IntegerField(db_index=True)
    current_price = models.TextField(default=0, null=True, blank=True)
    quantity = models.IntegerField(default=1, db_index=True)
    outlier_score_final = models.FloatField(null=True, blank=True)
    upper_outlier_score_final = models.FloatField(null=True, blank=True)
    median_price_final = models.FloatField(null=True, blank=True)
    item_savings_value = models.FloatField(null=True, blank=True)
    eprocure_total_value = models.FloatField(null=True, blank=True)
    item_code = models.CharField(max_length=100, blank=True, null=True)
    price_validity_months = models.IntegerField(default=12)
    unit_of_measure = models.TextField()
    current_supplier = models.TextField(blank=True, null=True)
    specification_1 = models.TextField(blank=True, null=True)
    specification_2 = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Request for Quotation Item"
        verbose_name_plural = "Request for Quotation Items"
        ordering = ["-id"]

    @property
    def unique_ref(self):
        return "{}_{}".format(self.category_id, self.item_number)

    @property
    def responses(self):
        return RFQItemResponse.objects.filter(rfq_item=self)

    @property
    def response_count(self):
        return self.responses.count()

    @property
    def average_price(self):
        total_item_bids = 0
        for response in self.responses:
            try:
                total_item_bids += float(show(response.total))
            except:
                total_item_bids += 0

        if total_item_bids == 0 or self.response_count < 1:
            return 0

        return total_item_bids / self.response_count

    @property
    def median_price(self):
        """Get the median reference point for purpose of eliminating outliers"""
        # todo get the media of the prices
        # if self.median_price_final == None or self.median_price_final == 0:
        prices = []
        for response in self.responses:
            if response.total_price is not None:
                # try:
                #     bid_price = float(show(response.total))
                # except:
                #     bid_price = 0
                bid_price = response.total_price
                if bid_price > 0:
                    prices.append(bid_price)
            else:
                bid_price = 0

        median = 0
        if len(prices) > 0:
            median = statistics.median(prices)
        self.median_price_final = median
        self.save()
        # else:
        #     median = self.median_price_final
        return median

    @property
    def outlier_score(self):
        # outlier 75% less than average
        # if self.outlier_score_final == None or self.outlier_score_final == 0:
        # outlier_score = 0.25 * self.median_price
        outlier_score = 0.50 * float(self.median_price)
        self.outlier_score_final = outlier_score
        self.save()
        # else:
        #     outlier_score = self.outlier_score_final

        return outlier_score

    @property
    def upper_outlier_score(self):
        # outlier 75% less than average
        # todo temporarily
        # if self.upper_outlier_score_final == None or self.outlier_score_final == 0:
        upper_outlier_score = 1.75 * self.median_price
        self.upper_outlier_score_final = upper_outlier_score
        self.save()
        # else:
        #     upper_outlier_score = self.upper_outlier_score_final

        return upper_outlier_score

    # below methods are used in reports you may add more
    @property
    def current_total(self):
        # get the item current total cost
        return round(float(self.current_price))

    @property
    def actual_current_total(self):
        # get the item current total cost
        return round(float(self.current_price) * self.quantity)

    def multi_item_tender_eprocure_suppliers(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.status_open:
            if responses is None:
                responses = self.responses
            responses = responses.order_by("total_price")
            lowest = responses.first()
            suppliers = []
            for response in responses:
                if response.total_price is not None:
                    # response_total = show(response.total)
                    response_total = response.total_price
                else:
                    response_total = 0

                # weighted_score = (response.value / lowest.value) * tender.financial_weight
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

    def eprocure_total(self, responses=None):
        if responses is None:
            responses = self.responses
        return round(self.eprocure_supplier_cost(responses), 2)

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

    def eprocure_supplier_cost(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.category.status_open:
            cheapest = 99999999999999999.9  # to reduce processing time to O(1)
            if responses is None:
                responses = self.responses
            for response in responses:
                if response.total_price is not None:
                    response_total = response.total_price
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

    def eprocure_suppliers(self, responses=None):
        """Returns the cheapest cost that is not outlier or 0"""
        if not self.rfq.status_open:
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

    def eprocure_supplier(self, responses=None):
        """Returns the cheapest supplier that is not an outlier in the item"""
        if responses is None:
            responses = self.responses
        cheapest_offer = self.eprocure_total(responses)
        for response in responses:
            if response.total is not None:
                try:
                    response_total = show(response.total)
                except:
                    response_total = 0
            else:
                response_total = 0
            if float(cheapest_offer) == response_total:
                return response.supplier
        return None

    def eprocure_supplier_company_name(self, responses=None):
        if responses is None:
            responses = self.responses
        eprocure_supplier = self.eprocure_supplier(responses)
        if eprocure_supplier is not None:
            return eprocure_supplier.supplier_name
        return "Unknown"

    def modified_lowest_cost(self, responses=None):
        """Returns the cheapest supplier cost that is not an outlier in the item"""
        if not self.rfq.status_open:
            if responses is None:
                responses = self.responses

            responses = responses.order_by("value")

            for response in responses:
                if response.total is not None:
                    try:
                        response_total = show(response.total)
                    except:
                        response_total = 0
                else:
                    response_total = 0

                if responses.count() <= 2:
                    cheapest_offer = responses.first()
                    try:
                        cheapest_offer = show(cheapest_offer.total)
                    except:
                        cheapest_offer = 0
                else:
                    if float(self.outlier_score) < response_total:
                        cheapest_offer = response_total

            return round(cheapest_offer, 2)

    def tendersure_eprocure_suppliers(self, responses=None):
        """
        Returns the cheapest cost that is not an outlier or 0
        """
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

            suppliers.append(
                {
                    "supplier_name": response.supplier.supplier_name,
                    "email": response.supplier.email,
                    "phone_no": response.supplier.phone_number,
                    "contact_name": response.supplier.contact_name,
                    "address_1": response.supplier.address_1,
                    "postal_address": response.supplier.supplier_name,
                    "tax_identification_number": response.supplier.tax_identification_number,
                    "country": response.supplier.country,
                    "city": response.supplier.city,
                    "price": response_total,
                }
            )
        sorted_suppliers = sorted(suppliers, key=lambda i: i["price"])
        tendersure_suppliers = sorted_suppliers[:3]

        return tendersure_suppliers


class SupplierResponse(BaseModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=True, on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, blank=False, null=True, on_delete=models.CASCADE
    )
    document_url = models.FileField(
        upload_to="Rfq/%Y/%m/%d",
        storage=PrivateMediaStorage(),
        validators=validators,
        blank=True,
        null=True,
        max_length=1000,
    )

    @property
    def full_document_url(self):
        response = None
        if self.document_url:
            response = get_document_url(f"{self.document_url}")
        return response


class RFQItemResponse(BaseModel):
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=True, on_delete=models.CASCADE
    )
    rfq_item = models.ForeignKey(
        RFQItem, blank=False, null=True, on_delete=models.CASCADE
    )
    total = models.TextField(null=True, blank=True)
    cell_data = models.TextField(null=True, blank=True, db_index=True)  # save json
    column_data = models.TextField(null=True, blank=True, db_index=True)  # save Json
    item_number = models.IntegerField(db_index=True)  # the item number in the excel
    value = models.BigIntegerField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, default=0
    )
    total_price = models.DecimalField(
        max_digits=20, decimal_places=2, null=True, default=0
    )

    class Meta:
        verbose_name = "Request for Quotation Item Response"
        verbose_name_plural = "Request for Quotation Item Responses"


class SupplierRfqTotal(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=False, null=False, on_delete=models.CASCADE
    )
    score = models.DecimalField(
        help_text="Total Score",
        max_digits=20,
        decimal_places=6,
        db_index=True,
        default=0,
    )
    has_outlier = models.BooleanField(default=False)
    has_blank = models.BooleanField(default=False, null=True, blank=True)
    # weighted score
    rfq_score = models.DecimalField(
        max_digits=20, decimal_places=6, db_index=True, default=0
    )
    rank = models.BigIntegerField(db_index=True, default=0)


class RfqInvitee(BaseModel):
    category = models.ForeignKey(
        Category, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        "suppliers.Supplier", blank=True, null=True, on_delete=models.CASCADE
    )
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "RFQ Category Invitee"
        verbose_name_plural = "RFQ Category Invitees"


class RFQCategoryReport(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, blank=True, null=True
    )
    category_rfq_pdf = models.FileField(
        upload_to="rfq/category/reports/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
    )
    financial = models.FileField(
        upload_to="rfq/category/reports/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "RFQ Category Reports"
        verbose_name_plural = "RFQ Categoty Reports"


class RFQJobReport(BaseModel):
    job = models.ForeignKey(Rfq, on_delete=models.CASCADE)
    job_savings = models.FileField(
        upload_to="rfq/job/reports/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
    )
    participation_report = models.FileField(
        upload_to="rfq/job/reports/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
    )
    job_lowest_item_cost = models.FileField(
        upload_to="rfq/job/reports/%Y/%m/%d",
        validators=validators,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "RFQ Job Reports"
        verbose_name_plural = "RFQ Job Reports"
