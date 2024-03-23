import datetime
from django.db.models import Q
from notifications.base.models import AbstractNotification
from django import apps
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from notifications.signals import notify
from django.core.mail import get_connection
from apps.core.utils import criteria_files, get_document_url
from backend.storage_backends import PrivateMediaStorage
from django.core.mail import EmailMultiAlternatives
from cryptography.fernet import Fernet


validators=[
            FileExtensionValidator(
                allowed_extensions=["pdf", "doc", "docx", "jpg", "png", "jpeg", "xlsx", "xls", "zip", "rar"]
            )
        ]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CategoryGroup(BaseModel):
    name = models.CharField(max_length=250)
    code = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category Group"
        verbose_name_plural = "Category Groups"

    def __str__(self):
        return self.name


class CategoryType(BaseModel):
    name = models.CharField(max_length=200)
    category_group = models.ForeignKey(
        CategoryGroup, blank=False, null=False, on_delete=models.CASCADE
    )
    innitials = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Category Type"
        verbose_name_plural = "Category types"

    def __str__(self):
        return self.innitials + " - " + self.name

    @property
    def old_suppliers(self):
        """return suppliers who ever participated in this category type in the old system"""
        old_suppliers = CategoryTypeSupplier.objects.filter(
            Q(category_type_id=self.id), Q(supplier=None))
        return old_suppliers

    @property
    def suppliers(self):
        """return suppliers who ever participated in this category type"""

        tender_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
                question__section__category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )
        prequal_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
                question__section__category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )
        rfq_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('rfq', 'RFQItem').objects.filter(
                category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )

        category_type_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=CategoryTypeSupplier.objects.filter(
                Q(category_type=self), ~Q(supplier=None)
            ).only('supplier_id').values('supplier_id')
        )

        suppliers = tender_suppliers.union(prequal_suppliers, rfq_suppliers, category_type_suppliers)
        return suppliers

    def suppliers_list(self, country=None):
        tender_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('tender', 'SupplierResponse').objects.filter(
                question__section__category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )
        prequal_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('prequal', 'SupplierResponse').objects.filter(
                question__section__category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )
        rfq_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=apps.apps.get_model('rfq', 'SupplierResponse').objects.filter(
                category__category_type_id=self.id
            ).only('supplier_id').values('supplier_id').distinct()
        )

        category_type_suppliers = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            id__in=CategoryTypeSupplier.objects.filter(
                Q(category_type=self), ~Q(supplier=None)
            ).only('supplier_id').values('supplier_id')
        )
        if country == None:
            registered_suppliers = tender_suppliers.union(prequal_suppliers, rfq_suppliers, category_type_suppliers)
            old_suppliers = self.old_suppliers
            data = {
                "registered_suppliers": registered_suppliers,
                "old_suppliers": old_suppliers,
                "supplier_count": len(old_suppliers) + len(registered_suppliers),
            }
            return data
        else:
            registered_suppliers = []
            s = tender_suppliers.union(prequal_suppliers, rfq_suppliers)
            if country == "Kenya":
                old_suppliers = CategoryTypeSupplier.objects.filter(
                    Q(category_type=self),
                    Q(supplier=None),
                    Q(Q(country=country) | Q(country=None)),
                )

                category_suppliers = CategoryTypeSupplier.objects.filter(
                    Q(category_type=self), ~Q(supplier=None), Q(Q(country=country) | Q(country=None)),
                )

                for supplier in s:
                    if supplier.country == country or supplier.country == None:
                        registered_suppliers.append(supplier)
                for supplier in category_suppliers:
                    registered_suppliers.append(supplier.supplier)
            else:
                old_suppliers = CategoryTypeSupplier.objects.filter(
                    Q(category_type=self),
                    Q(supplier=None),
                    Q(country=country),
                    Q(unsubscribe=False),
                )
                # for category in self.categories:
                category_suppliers = CategoryTypeSupplier.objects.filter(
                    Q(category_type=self), ~Q(supplier=None), Q(country=country), Q(unsubscribe=False),
                )
                for supplier in s:
                    if supplier.country == country:
                        registered_suppliers.append(supplier)
                for supplier in category_suppliers:
                    registered_suppliers.append(supplier.supplier)
            registered_suppliers = list(set(registered_suppliers))
            supplier_count = len(old_suppliers) + len(registered_suppliers)

            data = {
                "registered_suppliers": registered_suppliers,
                "old_suppliers": old_suppliers,
                "supplier_count": supplier_count,
            }
            print(data)
            return data


class CategoryTypeSupplier(BaseModel):
    category_type = models.ForeignKey(
        CategoryType, blank=False, null=False, on_delete=models.CASCADE
    )
    supplier = models.ForeignKey('suppliers.Supplier', blank=True, null=True, on_delete=models.CASCADE)
    company_name = models.TextField(blank=True, null=True)
    primary_email = models.TextField(blank=True, null=True)
    alternative_email = models.TextField(blank=True, null=True)
    primary_phone = models.TextField(blank=True, null=True)
    alternative_phone = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    unsubscribe = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        verbose_name = "Category Type Supplier"
        verbose_name_plural = "Category Type Suppliers"


class CategoryTypeSupplierLocation(BaseModel):
    category_type_supplier = models.ForeignKey(
        CategoryTypeSupplier, on_delete=models.CASCADE
    )
    location = models.CharField(max_length=500)

    class Meta:
        verbose_name = "Category Type Supplier Location"
        verbose_name_plural = "Category Type Supplier Locations"


class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = "Mpesa Call"
        verbose_name_plural = "Mpesa Calls"


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = "Mpesa Call Back"
        verbose_name_plural = "Mpesa Call Backs"


class PaybillBallance(BaseModel):
    transaction_id = models.TextField()
    transaction_number = models.TextField()
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    organisation_balance = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.TextField()

    class Meta:
        verbose_name = "Pay Bill Balance"
        verbose_name_plural = "Pay bill Balances"


class MpesaPayment(BaseModel):

    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    INVALID = 3

    TRANSACTION_STATUS = (
        (PENDING, _("Pending")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.TextField()
    payment_status = models.IntegerField(choices=TRANSACTION_STATUS, default=PENDING)

    class Meta:
        verbose_name = "Mpesa Payment"
        verbose_name_plural = "Mpesa Payments"

    def __str__(self):
        return self.first_name


class Payment(BaseModel):
    model = models.TextField()
    instance_id = models.BigIntegerField()
    timestamps = models.TextField()

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["id"]

    def __str__(self):
        return self.model + " " + str(self.instance_id)


class Currency(BaseModel):
    name = models.CharField(max_length=255)
    initials = models.CharField(max_length=200)

    def __str__(self):
        return str(self.initials)

class Job(BaseModel):
    company = models.ForeignKey('buyer.Company', on_delete=models.CASCADE)
    title = models.CharField(max_length=1000)
    unique_reference = models.CharField(max_length=1000)
    sourcing_activity = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    target_id = models.IntegerField()

    @property
    def is_open(self):
        if self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Prequalification')):
            c = apps.apps.get_model('prequal', 'Category').objects.filter(prequalification_id=self.target_id, is_open=True).first()
            if c != None:
                return True
            return False
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('asset_disposal', 'AssetDisposal')):
            c = apps.apps.get_model('asset_disposal', 'Category').objects.filter(asset_disposal_id=self.target_id, is_open=True).first()
            if c != None:
                return True
            return False
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Tender')):
            c = apps.apps.get_model('tender', 'Category').objects.filter(tender_id=self.target_id, is_open=True).first()
            if c != None:
                return True
            return False
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('rfq', 'RFQ')):
            c = apps.apps.get_model('rfq', 'Category').objects.filter(rfq_id=self.target_id, status_open=True).first()
            if c != None:
                return True
            return False
        else:
            return False

    @property
    def category_type_count(self):
        if self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Prequalification')):
            goods_count = 0
            services_count = 0
            works_count = 0

            categories = apps.apps.get_model('prequal', 'Category').objects.filter(prequalification_id=self.target_id, is_open=True)
            goods_count = categories.filter(category_type__category_group__name="Goods").count()
            services_count = categories.filter(category_type__category_group__name="Services").count()
            works_count = categories.filter(category_type__category_group__name="Works").count()
            
            context = {
                "goods": goods_count,
                "services": services_count,
                "works": works_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('asset_disposal', 'AssetDisposal')):
            goods_count = 0
            services_count = 0
            works_count = 0

            categories = apps.apps.get_model('asset_disposal', 'Category').objects.filter(asset_disposal_id=self.target_id, is_open=True)
            goods_count = categories.filter(category_type__category_group__name="Goods").count()
            services_count = categories.filter(category_type__category_group__name="Services").count()
            works_count = categories.filter(category_type__category_group__name="Works").count()
            
            context = {
                "goods": goods_count,
                "services": services_count,
                "works": works_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Tender')):
            goods_count = 0
            services_count = 0
            works_count = 0

            categories = apps.apps.get_model('tender', 'Category').objects.filter(tender_id=self.target_id, is_open=True)
            goods_count = categories.filter(category_type__category_group__name="Goods").count()
            services_count = categories.filter(category_type__category_group__name="Services").count()
            works_count = categories.filter(category_type__category_group__name="Works").count()
            
            context = {
                "goods": goods_count,
                "services": services_count,
                "works": works_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('rfq', 'RFQ')):
            goods_count = 0
            services_count = 0
            works_count = 0

            categories = apps.apps.get_model('rfq', 'Category').objects.filter(rfq_id=self.target_id, status_open=True)
            goods_count = categories.filter(category_type__category_group__name="Goods").count()
            services_count = categories.filter(category_type__category_group__name="Services").count()
            works_count = categories.filter(category_type__category_group__name="Works").count()
            
            context = {
                "goods": goods_count,
                "services": services_count,
                "works": works_count
            }
            return context

        else:
            goods_count = 0
            services_count = 0
            works_count = 0
            
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context

    @property
    def bidders(self):
        if self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Prequalification')):
            total_bidders_count = 0
            responsive_bidders_count = 0
            non_responsive_bidders_count = 0

            categories = apps.apps.get_model('prequal', 'Category').objects.filter(prequalification_id=self.target_id, is_open=True)
            for category in categories:
                responsive_bidders_count += category.responsive_bidder_count
                non_responsive_bidders_count += category.non_responsive_bids

            total_bidders_count = responsive_bidders_count + non_responsive_bidders_count
            
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('asset_disposal', 'AssetDisposal')):
            total_bidders_count = 0
            responsive_bidders_count = 0
            non_responsive_bidders_count = 0

            categories = apps.apps.get_model('asset_disposal', 'Category').objects.filter(asset_disposal_id=self.target_id, is_open=True)
            for category in categories:
                responsive_bidders_count += category.responsive_bidder_count
                non_responsive_bidders_count += category.non_responsive_bids

            total_bidders_count = responsive_bidders_count + non_responsive_bidders_count
            
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Tender')):
            total_bidders_count = 0
            responsive_bidders_count = 0
            non_responsive_bidders_count = 0

            categories = apps.apps.get_model('tender', 'Category').objects.filter(tender_id=self.target_id, is_open=True)
            for category in categories:
                responsive_bidders_count += category.responsive_bidder_count
                non_responsive_bidders_count += category.non_responsive_bids

            total_bidders_count = responsive_bidders_count + non_responsive_bidders_count
            
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context
        elif self.sourcing_activity == ContentType.objects.get_for_model(apps.apps.get_model('rfq', 'RFQ')):
            total_bidders_count = 0
            responsive_bidders_count = 0
            non_responsive_bidders_count = 0

            categories = apps.apps.get_model('rfq', 'Category').objects.filter(rfq_id=self.target_id, status_open=True)
            for category in categories:
                total_bidders_count += len(category.invited_suppliers)
                responsive_bidders_count += category.participants['count']

            non_responsive_bidders_count = total_bidders_count - responsive_bidders_count
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context

        else:
            total_bidders_count = 0
            responsive_bidders_count = 0
            non_responsive_bidders_count = 0
            
            context = {
                "total_bidders": total_bidders_count,
                "responsive_bidders": responsive_bidders_count,
                "non_responsive_bidders": non_responsive_bidders_count
            }
            return context


class CategoryOrder(BaseModel):
    PAID = 1
    PENDING = 2
    PROCESSING = 3
    FAILED = 4
    WITHDRAW = 5

    PAYMENT_STATUS_CHOICES = (
        (PAID, "Paid"),
        (PENDING, "Pending"),
        (PROCESSING, "Processing"),
        (FAILED, "Failed"),
        (WITHDRAW, "Withdrawn"),
    )

    # prequalification, tender, asset disposal
    target = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.CASCADE
    )
    category_id = models.IntegerField()
    # job_id = models.IntegerField()
    supplier = models.ForeignKey(
        'suppliers.Supplier', blank=False, null=False, on_delete=models.CASCADE
    )
    payment = models.ForeignKey(
        Payment, blank=True, null=True, on_delete=models.CASCADE
    )
    code = models.TextField(db_index=True)  # this should be simple
    payment_status = models.IntegerField(
        choices=PAYMENT_STATUS_CHOICES, default=PENDING, blank=False, null=False
    )

    class Meta:
        verbose_name = "Category Cart"
        verbose_name_plural = "Categories cart"

    def __str__(self):
        return self.code

    @property
    def category(self):
        if self.target == ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Category')):
            c = apps.apps.get_model('prequal', 'Category').objects.filter(id=self.category_id).first()
            return c
        elif self.target.model == "asset_disposal":
            c = apps.apps.get_model('asset_disposal', 'Category').objects.filter(id=self.category_id).first()
            return c
        elif self.target == ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Category')):
            c = apps.apps.get_model('tender', 'Category').objects.filter(id=self.category_id).first()
            return c
        else:
            return None


# class PesaPalCall(BaseModel):
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     description = models.TextField()
#     type = models.TextField()
#     reference = models.TextField()
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     email = models.EmailField()
#     phone_number = models.TextField()
#
#     class Meta:
#         verbose_name = "Pesapal Payment"
#         verbose_name_plural = "Pesapal Payments"
#
#     def __str__(self):
#         return self.first_name
#
#
# class PesaPalCallBack(BaseModel):
#     pesapal_merchant_reference = models.TextField()
#     pesapal_transaction_tracking_id = models.TextField()
#
#     class Meta:
#         verbose_name = "Pesapal Payment"
#         verbose_name_plural = "Pesapal Payments"
#
#     def __str__(self):
#         return "Transaction: {0}, Merchant_Reference: {1}".format(
#             self.pesapal_transaction_tracking_id, self.pesapal_merchant_reference
#         )


# class PesaPalPayment(models.Model):
#
#     PENDING = 0
#     COMPLETED = 1
#     FAILED = 2
#     INVALID = 3
#
#     TRANSACTION_STATUS = (
#         (PENDING, _("Pending")),
#         (COMPLETED, _("Completed")),
#         (FAILED, _("Failed")),
#     )
#     # VERIFICATION_STATUS_CHOICES = (
#     #     (CREATED, 'Created'),
#     #     (VERIFIED, 'Verified'),
#     # )
#     # pesapal_transaction = models.UUIDField(default=uuid.uuid4, editable=False)
#     merchant_reference = models.TextField(db_index=True)
#     amount = models.DecimalField(decimal_places=2, max_digits=10, default=0)
#     created = models.DateTimeField(auto_now_add=True)
#     payment_status = models.IntegerField(choices=TRANSACTION_STATUS, default=PENDING)
#     payment_method = models.CharField(max_length=24, null=True)
#
#     class Meta:
#         unique_together = (("merchant_reference", "pesapal_transaction"),)
#         verbose_name = "Pesapal Payment"
#         verbose_name_plural = "Pesapal Payments"
#         pass
#
#     def __str__(self):
#         return "Transaction: {0}, Merchant_Reference: {1}".format(
#             self.pesapal_transaction, self.merchant_reference
#         )


class CellulantPayment(BaseModel):
    accountNumber = models.TextField()
    currencyCode = models.TextField()
    checkoutRequestID = models.TextField()
    requestAmount = models.DecimalField(max_digits=10, decimal_places=2)
    amountPaid = models.DecimalField(max_digits=10, decimal_places=2)
    merchantTransactionID = models.TextField()
    requestDate = models.TextField()
    requestStatusDescription = models.TextField()
    MSISDN = models.TextField()

    class Meta:
        verbose_name = "Cellulant Payment"
        verbose_name_plural = "Cellulant Payments"

    def __str__(self):
        return str(self.id) + " - " + self.merchantTransactionID


class UserAudit(BaseModel):
    user = models.ForeignKey(
        User,
        related_name="user_audit",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    ip_address = models.TextField()
    browser = models.TextField(db_index=True)
    operating_system = models.TextField()
    timestamps = models.TextField(db_index=True)
    others = models.TextField(null=True)

    class Meta:
        verbose_name = "User audit"
        verbose_name_plural = "Users Audits"

    # def identify_browser(self, user_agent):
    #     user_agent = parse(user_agent)
    #     browser = (
    #         user_agent.browser.family + " version " + user_agent.browser.version_string
    #     )
    #     return browser
    #
    # def identify_os(self, user_agent):
    #     user_agent = parse(user_agent)
    #     device = user_agent.is_pc and "PC" or user_agent.device.family
    #     os = ("%s %s" % (user_agent.os.family, user_agent.os.version_string)).strip()
    #     return " / ".join([device, os])
    #
    # def readable_timestamp(self):
    #     date_time_str = self.timestamps
    #     # date_time_str =
    #     try:
    #         date_time_obj = datetime.datetime.strptime(
    #             date_time_str[:-13], "%Y-%m-%d %H:%M:%S"
    #         )
    #         tz = pytz.timezone("Africa/Nairobi")
    #         date_time_obj = date_time_obj.replace(tzinfo=datetime.timezone.utc)
    #         date_time_obj = date_time_obj.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S")
    #         # print()
    #     except:
    #         date_time_obj = self.timestamps
    #     return date_time_obj


class Country(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"

    def __str__(self):
        return self.name


class Notifications(AbstractNotification):
    AbstractNotification._meta.get_field("recipient").blank = True
    AbstractNotification._meta.get_field("recipient").null = True
    AbstractNotification._meta.get_field("actor_content_type").blank = True
    AbstractNotification._meta.get_field("actor_content_type").null = True
    AbstractNotification._meta.get_field("actor_object_id").blank = True
    AbstractNotification._meta.get_field("actor_object_id").null = True
    AbstractNotification._meta.get_field("actor").blank = True
    AbstractNotification._meta.get_field("actor").null = True

    TYPES = Choices(
        "all",
        "paid",
        "potential",
        "qualified",
        "unqualified",
        "specific",
        "broadcast",
        "responsive",
        "non-responsive",
    )
    type_class = models.CharField(
        choices=TYPES, max_length=20, null=True, default="broadcast"
    )

    class Meta(AbstractNotification.Meta):
        abstract = False

def notification_files(instance, filename):
    # file will be uploaded to MEDIA_ROOT/notification_documents/company_name/action_object_content_type/supplier_company_name/notification_id/filename
    company_name = apps.apps.get_model('buyer', 'Company').objects.get(
        id=int(instance.notification.actor_object_id)).company_name.replace(" ", "_")

    supplier_company_name = (
        instance.notification.recipient.supplier.company_name.replace(" ", "_")
    )

    # if instance.notification.action_object_content_type.model == "category":
    #     # cator for all modules
    #     category = Category.objects.filter(
    #         id=int(instance.notification.action_object_object_id)
    #     ).first()
    #     if category is not None:
    #         typename = category.name
    # elif instance.notification.action_object_content_type.model == "job":
    #     job = Job.objects.get(id=int(instance.notification.action_object_object_id))
    #     typename = job.job_code

    typename = ''

    notification_id = str(instance.notification.id)
    notification_documents = "notification_documents"
    return "%s/%s/%s/%s/%s/%s/%s" % (
        notification_documents,
        company_name,
        instance.notification.action_object_content_type,
        typename,
        supplier_company_name,
        notification_id,
        filename,
    )


class NotificationDocument(BaseModel):
    name = models.CharField(
        default="Unknown File Name", null=True, blank=True, max_length=250
    )
    document_url = models.FileField(
        upload_to=notification_files,
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )
    notification = models.ForeignKey(
        Notifications, blank=False, null=False, on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = "Notification Documents"
        verbose_name_plural = "Notification Documents"


# help emails for countries
class HelpContact(BaseModel):
    country = models.ForeignKey(Country, null=True, blank=True, on_delete=models.CASCADE)
    help_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=100)
    country_calling_code = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = "Help Contact"
        verbose_name_plural = "Help Contacts"


class CurrentSupplier(BaseModel):
    """
    Model for a company's current suppliers
    """

    company = models.ForeignKey('buyer.Company', null=True, on_delete=models.CASCADE)
    target = models.ForeignKey(ContentType, null=True, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    job_id = models.IntegerField()
    supplier_email = models.CharField(max_length=256, null=True, blank=True)
    supplier_name = models.CharField(max_length=256, null=True, blank=True)
    supplier_phone = models.CharField(max_length=256, null=True)
    alternative_email = models.CharField(max_length=256, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.supplier_email} - Job {self.job_id} - Category {self.category_id}"

    class Meta:
        verbose_name = "CurrentSupplier"
        verbose_name_plural = "CurrentSupplier"

    @property
    def category(self):
        if self.target == ContentType.objects.get_for_model(apps.apps.get_model('prequal', 'Category')):
            c = apps.apps.get_model('prequal', 'Category').objects.filter(id=self.category_id).first()
            return c
        elif self.target.model == "asset_disposal":
            c = apps.apps.get_model('asset_disposal', 'Category').objects.filter(id=self.category_id).first()
            return c
        elif self.target == ContentType.objects.get_for_model(apps.apps.get_model('tender', 'Category')):
            c = apps.apps.get_model('tender', 'Category').objects.filter(id=self.category_id).first()
            return c
        else:
            return None

    @property
    def participation_status(self):
        status = ""
        supplier_email_domain = self.supplier_email.split('@')[0] 
        paid_categories = CategoryOrder.objects.filter(            
            category_id=self.category_id,
            payment_status=CategoryOrder.PAID,
        ) 
        if supplier_email_domain in ['gmail.com', 'yahoo.com']:
            paid_categories = paid_categories.filter(
                supplier__email=self.supplier_email,
            )            
        else:
            paid_categories = paid_categories.filter(
                supplier__email__endswith=self.supplier_email,
            )
            
        if paid_categories.count() == 0:
            status = "Not Participated"
        else:
            status = "Participated"

        return status

    def get_current_supplier_pin(self, company_name, email):
        """
        Get current supplier by company_name or email
        :return: tax_pin
        """
        supplier = apps.apps.get_model('suppliers', 'Supplier').objects.filter(
            Q(company_name__iexact=company_name) | Q(username=email)
        ).first()
        if supplier is not None:
            return supplier.kra_pin_number
        else:
            return "None"

    def get_tax_pin(self):
        tax_pin = self.get_current_supplier_pin(
            company_name=self.supplier_name, email=self.supplier_email
        )
        if tax_pin is None:
            tax_pin = "None"

        return tax_pin


# class Task(BaseModel):
#     name = models.CharField(max_length=3000)
#     task_id = models.IntegerField()
#     total = models.IntegerField()
#     current = models.IntegerField()
#     percentage = models.DecimalField(decimal_places=2, max_digits=15)


class CriteriaCountry(BaseModel):
    name = models.CharField(max_length=250)


class CategoryTypeCriteria(BaseModel):
    criteria_country = models.ForeignKey(CriteriaCountry, on_delete=models.CASCADE)
    category_type = models.ForeignKey(CategoryType, on_delete=models.CASCADE)
    file_url = models.FileField(
        upload_to=criteria_files, validators=validators,
        blank=True, null=True, max_length=3000,
        # storage=PrivateMediaStorage(),
    )


def upload_supplier_receipts(instance, filename):
    return "%s/%s/%s" % (
        "supplier_receipts",
        instance.supplier.company_name.replace(" ", "_"),
        filename,
    )


class SupplierReceipt(BaseModel):
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
    supplier = models.ForeignKey(
        'suppliers.Supplier', on_delete=models.CASCADE, related_name="receipts"
    )
    mode_of_payment = models.CharField(max_length=20, blank=True, null=True)
    reference = models.CharField(max_length=256, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField()
    receipt = models.FileField(
        upload_to=upload_supplier_receipts,
        validators=validators,
        storage=PrivateMediaStorage(),
        blank=True,
        null=True,
        max_length=1000,
    )

    class Meta:
        verbose_name = "Supplier Receipt"
        verbose_name_plural = "Supplier Receipts"

    def __str__(self) -> str:
        return f"Receipt for {self.supplier.company_name}"

    @property
    def full_document_url(self):
        response = None
        if self.receipt:
            response = get_document_url(f"{self.receipt}")
        return response

    @property
    def associated_category(self):
        order = CategoryOrder.objects.filter(code=self.reference).first()
        if order is not None:
            category = order.category
            job = category.job.job_title
            job_title = job.split(" ")[:4]
            job_title = " ".join(map(str, job_title))

            return job_title
        else:
            return "N/A"


class EmailOut(BaseModel):
    REMINDER = 1

    TYPE_CHOICES = (
        (REMINDER, 'Reminder'),
    )
    subject = models.CharField(max_length=3000)
    to = models.EmailField()
    body = models.TextField()
    message = models.TextField()
    target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    type = models.IntegerField(choices=TYPE_CHOICES, default=REMINDER)
    sent = models.BooleanField(default=False)
    error = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Email Out"
        verbose_name_plural = "Emails Out"


class SmsOutManager(models.Manager):
    def bulk_create(self, objs, **kwargs):
        a = super(models.Manager, self).bulk_create(objs, **kwargs)
        for i in objs:
            i.save()
        return a


class SmsOut(BaseModel):
    objects = SmsOutManager()
    phone_number = models.CharField(max_length=100)
    text_message = models.TextField()
    short_code = models.CharField(max_length=100, default="TENDERSURE")
    target = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    category_id = models.IntegerField()
    unique_identifier = models.CharField(max_length=3000)
    sent = models.BooleanField(default=False)
    response = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Sms Out"
        verbose_name_plural = "Sms Out"


class EmailConfiguration(BaseModel):
    """
    Create Email configuration for every buyer
    """

    company = models.ForeignKey('buyer.Company', on_delete=models.CASCADE)
    email_host = models.CharField(max_length=250)
    host_password = models.TextField()
    email_username = models.CharField(max_length=256)
    email_port = models.CharField(max_length=256)
    default_from_email = models.CharField(max_length=256, blank=True)
    email_use_tls = models.BooleanField(default=False, blank=True)
    email_use_ssl = models.BooleanField(default=False, blank=True)
    app_password = models.TextField(default="", blank=True)
    # enc_password = models.BinaryField(blank=True)
    # enc_app_password = models.BinaryField(blank=True)

    def __str__(self) -> str:
        return f"{self.company}, {self.email_host}"

    def save(self, *args, **kwargs):
        self.generate_key()
        self.host_password = self.encrypt_decrypt_fields(
            self.host_password, encrypt=True
        )
        self.app_password = self.encrypt_decrypt_fields(self.app_password, encrypt=True)
        super(EmailConfiguration, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "EmailConfiguration"
        verbose_name_plural = "Email Configurations"

    @property
    def get_email_connection(self):
        """
        Get email connection by authenticating using username and password
        """
        connection = get_connection(
            backend="django.core.mail.backends.smtp.EmailBackend",
            host=self.email_host,
            port=self.email_port,
            username=self.email_username,
            password=self.encrypt_decrypt_fields(self.host_password, encrypt=False),
            use_tls=self.email_use_tls,
        )
        return connection

    def generate_key(self):
        """
        Generate key and save
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)

    def load_key(self):
        return open("secret.key", "rb").read()

    def encrypt_decrypt_fields(self, message, encrypt=False):
        """
        Encrypt and Decrypt sensitive fields (password/app_password)
        """
        key = self.load_key()
        fernet = Fernet(key)
        if encrypt is True:
            encryted_msg = fernet.encrypt(message.encode())
            return encryted_msg.decode()
        else:
            message = message.encode()
            decrypted_msg = fernet.decrypt(message).decode()
            return decrypted_msg

    def send_email(self, subject, body, bcc=[]):
        """
        Send an email using connection established
        """
        connection = self.get_email_connection
        open_connect = connection.open()
        if open_connect is True:
            email = EmailMultiAlternatives(
                subject=subject,
                body=body,
                from_email=self.email_username,
                bcc=bcc,
                connection=connection,
            )
            email.attach_alternative(body, "text/html")
            email.send()

            connection.close()
        else:
            return {"sending emails failed"}