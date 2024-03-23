import datetime
import os
from pathlib import Path

import requests
from django.db import models
from apps.core.models import BaseModel
from django.core.validators import FileExtensionValidator
from backend.storage_backends import PrivateMediaStorage


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


class AssetDisposal(BaseModel):
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("final", "Published"),
    )
    title = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default="draft")
    lang_en = models.BooleanField(default=True)
    show_bids = models.BooleanField(default=True)
    advert = models.FileField(
        upload_to="job/advert",
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=3000,
    )
    current_suppliers = models.FileField(upload_to='')
    # company = models.ForeignKey()
    # approved_by = models.ForeignKey()
    # created_by = models.ForeignKey()

    class Meta:
        verbose_name = "Asset Disposal Job"
        verbose_name_plural = "Asset Disposal Jobs"

    def __str__(self):
        return f"{self.title} : {self.unique_reference}"


class Category(BaseModel):
    name = models.CharField(max_length=1000)
    trans_name = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    totals_column = models.CharField(max_length=1000)
    instructions = models.TextField()
    bid_charge = models.DecimalField(max_digits=20, decimal_places=2)
    is_open = models.BooleanField(default=False)
    is_invite_notification_sent = models.BooleanField(default=False)
    is_self_evaluate = models.BooleanField(default=False)
    is_invite_only = models.BooleanField(default=False)
    allowed_staff = models.BooleanField(default=False)
    opening_date = models.DateTimeField()
    closing_date = models.DateTimeField()
    evaluation_date = models.DateTimeField()
    # category_type = models.ForeignKey()
    # currency = models.ForeignKey()
    asset_disposal = models.ForeignKey(AssetDisposal, on_delete=models.CASCADE)
    items_template = models.FileField(upload_to='')

    class Meta:
        verbose_name = "Asset disposal category"
        verbose_name_plural = "Asset disposal categories"

    def __str__(self):
        return f"{self.name} : {self.unique_reference}"


class Item(BaseModel):
    name = models.CharField(max_length=1000)
    number = models.IntegerField()
    quantity = models.IntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class SupplierResponse(BaseModel):
    # supplier = models.ForeignKey()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    response_template = models.FileField(
        upload_to="Rfq/%Y/%m/%d", validators=validators,
        storage=PrivateMediaStorage(), blank=True, null=True, max_length=1000,
    )

    def relative_quotation_url(self):
        excel_path = "{}".format(self.response_template)
        A = PrivateMediaStorage()
        headers = {"ResponseContentDisposition": f"attachment;"}
        time = datetime.datetime.now()
        file_url = A.url(
            f"{excel_path}", expire=300, parameters=headers, http_method="GET"
        )

        dir_name = Path("media/temp/{}/{}/{}".format(time.year, time.month, time.day))
        dir_name.mkdir(parents=True, exist_ok=True)
        file_name = os.path.basename(f"{excel_path}")
        filepath = "{}/{}".format(dir_name, file_name)

        my_file = Path(filepath)
        if my_file.is_file():
            return filepath

        r = requests.get(file_url)
        with open("{}".format(filepath), "wb") as f:
            f.write(r.content)

        return filepath


class SupplierItemResponse(BaseModel):
    supplier_response = models.ForeignKey(SupplierResponse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, blank=False, null=True, on_delete=models.CASCADE)
    total = models.TextField(null=True)
    cell_data = models.TextField(null=True)
    column_data = models.TextField(null=True)
    item_number = models.IntegerField()
    value = models.BigIntegerField(null=True)


class SupplierCategoryTotal(BaseModel):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # supplier = models.ForeignKey( on_delete=models.CASCADE)
    total_bid = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    category_score = models.DecimalField(max_digits=20, decimal_places=6, default=0)
    rank = models.BigIntegerField(default=0)

    class Meta:
        verbose_name = "Supplier AssetDisposalCategory Total"
        verbose_name_plural = "Supplier AssetDisposalCategory Totals"

    @property
    def supplier_response(self):
        return SupplierResponse.objects.filter(
            supplier_id=self.supplier_id, category_id=self.category_id
        )


class CategoryReport(BaseModel):
    financial_report = models.FileField(
        null=True, blank=True, validators=validators, storage=PrivateMediaStorage(),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Category Report"
        verbose_name_plural = "Category Reports"


class JobReport(BaseModel):
    asset_disposal = models.ForeignKey(AssetDisposal, on_delete=models.CASCADE)
    summary_report = models.FileField(
        null=True, blank=True, max_length=3000,
        validators=validators, storage=PrivateMediaStorage(),
    )

    class Meta:
        verbose_name = "Asset Disposal Report"
        verbose_name_plural = "Asset Disposal Reports"