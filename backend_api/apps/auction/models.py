import pytz
import os
from django.utils import timezone
from django import apps
from django.contrib.auth.models import User

from django.db import models
from django.conf import settings
from apps.core.models import BaseModel, CategoryType, User, Currency
from django.core.validators import FileExtensionValidator
from apps.core.utils import show, get_document_url
from apps.suppliers.models import Supplier
from backend.storage_backends import PrivateMediaStorage
from django.utils.translation import gettext_lazy as _


REVERSE = "Reverse Auction"
FORWARD = "Forward Auction"

AUCTION_CHOICES = ((REVERSE, "Reverse Auction"), (FORWARD, "Forward Auction"))

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

validators_image = [
    FileExtensionValidator(
        allowed_extensions=[
            "jpg", 
            "png", 
            "jpeg"
        ]
    )
]

validators_excel = [
    FileExtensionValidator(
        allowed_extensions=[
            "xlsx",
            "xls",
            "csv",
        ]
    )
]

def get_auction_image_path(instance, filename):
    return os.path.join("auction/images", str(instance.id), filename)

class Auction(BaseModel):

    SINGLE_NOTE = "Single note"
    MULTI_NOTE = "Multi note"


    PRICING_CHOICES = ((SINGLE_NOTE, "Single note"), (MULTI_NOTE, "Multi note"))
    
    name = models.CharField(max_length=200, db_index=True, unique=True)
    company = models.ForeignKey('buyer.Company', db_index=True, on_delete=models.CASCADE)
    auction_type = models.CharField(
        max_length=50, choices=AUCTION_CHOICES, null=True, default=REVERSE
    )
    pricing_method = models.CharField(
        max_length=50, choices=PRICING_CHOICES, null=True, blank=True, default=MULTI_NOTE
    )
    opening_date = models.DateTimeField(db_index=True)
    closing_date = models.DateTimeField(db_index=True)
    status_open = models.BooleanField(default=False)
    closed_auction = models.BooleanField(default=True)
    category_type = models.ForeignKey(
        CategoryType, null=True, blank=True,  on_delete=models.SET_NULL
    )
    overtime_count = models.IntegerField(default=0, blank=True, null=True)
    # keep track of the counter
    overtime_counter = models.IntegerField(default=0, blank=True, null=True, help_text=_("Keep track of the counter."),)
    overtime_duration = models.IntegerField(blank=True, null=True)
    # user id
    created_by = models.ForeignKey(
        User, related_name="user_auction",
        blank=True, null=True,on_delete=models.SET_NULL,
    )
    created_by_email = models.EmailField(
        default="eprocure@qedsolutions.co.ke", null=False, blank=False
    )
    supporting_document = models.FileField(
        upload_to="auctions/supporting_document/%Y/%m/%d",
        blank=True,
        null=True, validators=validators,
        # storage=PrivateMediaStorage()
    )
    excel_template = models.FileField(
        upload_to="auctions/excel_items/%Y/%m/%d",
        blank=True,
        null=True, max_length=3000, validators=validators_excel,
        # storage=PrivateMediaStorage()
    )
    is_open = models.BooleanField(default=False, blank=True, null=True)
    invite_only = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        tz = pytz.timezone(settings.TIME_ZONE)
        if self.closing_date.tzinfo is None:
            if timezone.now() > tz.localize(self.closing_date):
                self.status_open = False
                super(Auction, self).save(*args, **kwargs)
            else:
                super(Auction, self).save(*args, **kwargs)
        else:
            if timezone.now() > self.closing_date:
                self.status_open = False
                super(Auction, self).save(*args, **kwargs)
            else:
                super(Auction, self).save(*args, **kwargs)
    
    @property
    def items(self):
        return AuctionItems.objects.filter(auction =self).count()

    @property
    def cummulative_reserve_price(self):
        cumm_reserve = AuctionItems.objects.filter(auction__id=self.id).aggregate(
            models.Sum('reserve_price'))['reserve_price__sum']

        return cumm_reserve
    
    @property
    def participants(self):
        suppliers = []
        responses = AuctionItemResponses.objects.filter(auction_item__auction_id=self.id).values_list(
            "supplier_id", flat=True
        )
        if responses.count() == 0:
            for response in responses:
                supplier = response.supplier
                if supplier not in suppliers:
                    suppliers.append(supplier)
            participants = set(suppliers)
            return {"participants": participants, "count": len(participants)}
    
    @property
    def has_bidding_activity(self):
        activity = AuctionItemResponses.objects.filter(auction_item__auction_id=self.id)
        if activity.count() > 0:
            return True
        else:
            return False
    
    @property
    def excel_response_url(self):
        if self.excel_template is not None:
            response = get_document_url(f"{self.excel_template}")
        return response

    @property
    def supporting_document_response_url(self):
        if self.supporting_document is not None:
            response = get_document_url(f"{self.supporting_document}")
        return response
    
    @property
    def item_names(self):
        return AuctionItems.objects.filter(auction =self).values_list('name', flat=True)

class AuctionInvitee(BaseModel):
    auction = models.ForeignKey(
        Auction, blank=False, null=False, related_name='invitee_auction', on_delete=models.CASCADE
    )
    supplier = models.ForeignKey(
        Supplier, blank=True, null=True, related_name='invitee_auction_supplier', on_delete=models.SET_NULL
    )
    email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "Auction Invitee"
        verbose_name_plural = "Auction Invitees"

class AuctionItems(BaseModel):
    auction = models.ForeignKey(
        Auction, on_delete=models.CASCADE, related_name='auction_items'
    )
    name = models.CharField(max_length=200)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    reserve_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE, related_name='auction_item_currency', 
        blank=True, null=True
    )
    quantity = models.IntegerField(default=1)
    minimum_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    minimum_increment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    minimum_decrement = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    best_bid_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 ,null=True, blank=True
    )
    created_by = models.ForeignKey(
        User, related_name="user_auction_item", blank=True,
        null=True, on_delete=models.SET_NULL,
    )
    created_by_email = models.EmailField(
        default="eprocure@qedsolutions.co.ke", null=False, blank=False
    )
    main_image = models.ImageField(
        upload_to=get_auction_image_path, validators=validators_image,
        blank=True, null=True,
        # storage=PrivateMediaStorage()
    )

    class Meta:
        verbose_name = "Auction Item"
        verbose_name_plural = "Auction Items"

    def __str__(self):
        return self.name

    @property
    def item_closing_time(self):
        return self.auction.closing_date
    
    @property
    def item_opening_time(self):
        return self.auction.opening_date
    
    @property
    def item_status(self):
        return self.auction.is_open

    @property
    def fetch_best_bid_price(self):
        item_bids_queryset = AuctionItemResponses.objects.filter(auction_item=self.id)
        if self.auction.auction_type == REVERSE:
            return item_bids_queryset.aggregate(models.Min('bid_price'))            
        if self.auction.auction_type == FORWARD:
            return item_bids_queryset.aggregate(models.Max('bid_price'))
    
    @property
    def has_bidding_activity(self):
        activity = AuctionItemResponses.objects.filter(auction_item_id=self.id)
        if activity.count() > 0:
            return True
        else:
            return False

    @property
    def best_bidder(self):
        item_bids_queryset = AuctionItemResponses.objects.filter(auction_item=self.id)
        if self.auction.auction_type == REVERSE:
            if len(item_bids_queryset.values_list('supplier_id__company_name').annotate(models.Min('bid_price')).order_by('bid_price')) > 0:
                return item_bids_queryset.values_list('supplier_id__company_name').annotate(models.Min('bid_price')).order_by('bid_price')[0][0]
            else:
                return ''
        if self.auction.auction_type == FORWARD:
            if len(item_bids_queryset.values_list('supplier_id__company_name').annotate(models.Max('bid_price')).order_by('bid_price')) > 0: 
                return item_bids_queryset.values_list('supplier_id__company_name').annotate(models.Max('bid_price')).order_by('bid_price')[0][0]
            else:
                return ''

class AuctionItemImage(BaseModel):
    item = models.ForeignKey(
        AuctionItems, null=True, blank=True, on_delete=models.CASCADE, related_name='auction_item_images'
    )
    image = models.ImageField(
        upload_to=get_auction_image_path, validators=validators_image,
        blank=True, null=True,
        # storage=PrivateMediaStorage()
    )
    thumbnail = models.ImageField(
        upload_to=get_auction_image_path, validators=validators_image,
        blank=True, null=True,
        # storage=PrivateMediaStorage()
    )
    class Meta:
        verbose_name = "Auction Item Image"

    def __str__(self):
        return self.item.name

class AuctionItemResponses(BaseModel):
    auction_item = models.ForeignKey(
        AuctionItems, null=False, blank=False, on_delete=models.CASCADE, related_name='auction_item_responses'
    )
    supplier = models.ForeignKey(
        Supplier, blank=True, null=True, on_delete=models.SET_NULL
    )
    bid_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    rank = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Auction Item Response"
        verbose_name_plural = "Auction Item Responses"

    def __str__(self):
        return self.auction_item.name + " | " + self.supplier.first_name + " | " + str(self.bid_price)
    
    @property
    def supplier_name(self):
        if self.supplier:
            return self.supplier.company_name
        else:
            return ''

# Keeps Track of the auction bids 
class AuctionItemResponsesTracking(BaseModel):
    auction_item_response =  models.ForeignKey(
        AuctionItemResponses, null=False, blank=False, on_delete=models.CASCADE, related_name='auction_item_response_tracking'
    )
    bid = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        verbose_name = "Auction Item Response Tracking"
        verbose_name_plural = "Auction Item Responses Tracking"
        constraints = [
            models.UniqueConstraint(
            name='unique_bid',
            fields=["auction_item_response", "bid"]),
        ]

    def __str__(self):
        return str(self.auction_item_response) + " | " + str(self.bid)

def auction_documents(instance, filename):
    # file will be uploaded to MEDIA_ROOT/company_name/job_code/category_unique_reference/filename

    return "%s/%s/%s/%s" % (
        instance.company.company_name.replace(" ", "_"),
        instance.name,
        instance.supplier.company_name.replace("", "_"),
        filename,
    )

class AuctionTotalItemResponse(BaseModel):
    auction = models.ForeignKey(Auction, null=False, blank=False, on_delete=models.CASCADE)
    supplier = models.ForeignKey(Supplier, null=True, blank=True, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    excel_url = models.FileField(
        upload_to=auction_documents, validators=[FileExtensionValidator(allowed_extensions=["xlsx", "xls"])],
        storage=PrivateMediaStorage(), blank=True, null=True,max_length=1000
    )

    class Meta:
        verbose_name = "Auction Total Item Reponse"
        verbose_name_plural = "Auction Total Item Reponses"

    def __str__(self):
        return self.auction.name + "|" + self.supplier.first_name
    
    @property
    def full_excel_url(self):
        response = None
        if self.document_url:
            response = get_document_url(f"{self.document_url}")
        return response