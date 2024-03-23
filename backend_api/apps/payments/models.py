from django.db import models

from apps.core.models import BaseModel
from django.utils.translation import gettext_lazy as _


class DpoToken(BaseModel):
    response_code = models.CharField(max_length=250)
    explanation = models.TextField()
    token = models.TextField(null=True, blank=True)
    reference = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "DpoToken",
        verbose_name_plural = "DpoTokens"


class DpoTokenCallBack(BaseModel):
    transaction_id = models.CharField(max_length=500)
    ccd_approval = models.CharField(max_length=500)
    transaction_token = models.CharField(max_length=500)
    reference = models.CharField(max_length=500)

    class Meta:
        verbose_name = 'DpoTokenCallBack'
        verbose_name_plural = 'DpoTokenCallBacks'


class DpoPayment(BaseModel):
    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    INVALID = 3
    PROCESSING = 4

    TRANSACTION_STATUS = (
        (PENDING, _("Pending")),
        (COMPLETED, _("Completed")),
        (FAILED, _("Failed")),
    )

    response_code = models.CharField(max_length=250)
    explanation = models.TextField(null=True, blank=True)
    customer_name = models.CharField(max_length=500, null=True, blank=True)
    customer_credit = models.CharField(max_length=500, null=True, blank=True)
    transaction_approval = models.CharField(max_length=500, null=True, blank=True)
    transaction_currency = models.CharField(max_length=500, null=True, blank=True)
    transaction_amount = models.CharField(max_length=500, null=True, blank=True)
    fraud_alert = models.CharField(max_length=500, null=True, blank=True)
    fraud_explanation = models.CharField(max_length=500, null=True, blank=True)
    transaction_net_amount = models.CharField(max_length=500, null=True, blank=True)
    transaction_settlement_date = models.CharField(max_length=500, null=True, blank=True)
    transaction_rolling_reverse_amount = models.CharField(max_length=500, null=True, blank=True)
    transaction_rolling_reverse_date = models.CharField(max_length=500, null=True, blank=True)
    customer_phone = models.CharField(max_length=500, null=True, blank=True)
    customer_country = models.CharField(max_length=500, null=True, blank=True)
    customer_address = models.CharField(max_length=500, null=True, blank=True)
    customer_city = models.CharField(max_length=500, null=True, blank=True)
    customer_zip = models.CharField(max_length=500, null=True, blank=True)
    mobile_payment_request = models.CharField(max_length=500, null=True, blank=True)
    reference = models.CharField(max_length=500, null=True, blank=True)
    payment_status = models.IntegerField(choices=TRANSACTION_STATUS, default=PENDING)

    class Meta:
        verbose_name = 'DpoPayment'
        verbose_name_plural = 'DpoPayments'

#
# class MpesaCall(BaseModel):
#     ip_address = models.TextField()
#     caller = models.TextField()
#     conversation_id = models.TextField()
#     content = models.TextField()
#
#     class Meta:
#         verbose_name = "Mpesa Call"
#         verbose_name_plural = "Mpesa Calls"
#
#
# class MpesaCallBack(BaseModel):
#     ip_address = models.TextField()
#     caller = models.TextField()
#     conversation_id = models.TextField()
#     content = models.TextField()
#
#     class Meta:
#         verbose_name = "Mpesa Call Back"
#         verbose_name_plural = "Mpesa Call Backs"
#
#
# class PayBillBalance(BaseModel):
#     transaction_id = models.TextField()
#     transaction_number = models.TextField()
#     transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     organisation_balance = models.DecimalField(max_digits=10, decimal_places=2)
#     timestamp = models.TextField()
#
#     class Meta:
#         verbose_name = "Pay Bill Balance"
#         verbose_name_plural = "Pay bill Balances"
#
#
class MpesaPayment(BaseModel):

    PENDING = 0
    COMPLETED = 1
    FAILED = 2
    INVALID = 3

    TRANSACTION_STATUS = (
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (FAILED, "Failed"),
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

class Stk(BaseModel):
    merchant_request_id = models.CharField(max_length=250,null=True)
    checkout_request_id = models.CharField(max_length=250,null=True)
    reference = models.TextField()
    result_code = models.IntegerField(null=True)
    result_desc = models.CharField(max_length=250,null=True)
    amount = models.FloatField(null=True,blank=True)
    mpesa_confirmation_code = models.CharField(max_length=250,null=True)
    balance = models.CharField(max_length=250,null=True)
    transaction_date = models.CharField(max_length=250,null=True)
    phone_number = models.CharField(max_length=250,null=True)

    class Meta:
        ordering = ['-transaction_date']

    def __str__(self):
        return str(self.checkout_request_id)

class CellulantWebhook(BaseModel):
    checkoutRequestID = models.CharField(max_length=200, blank=True, null=True)
    merchantTransactionID = models.CharField(max_length=200, blank=True, null=True)
    requestStatusCode = models.IntegerField(blank=True, null=True)
    requestAmount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    requestStatusDescription = models.CharField(max_length=200, blank=True, null=True)
    MSISDN = models.CharField(max_length=200, blank=True, null=True)
    serviceCode = models.CharField(max_length=200, blank=True, null=True)
    accountNumber = models.CharField(max_length=200, blank=True, null=True)
    currencyCode = models.CharField(max_length=200, blank=True, null=True)
    amountPaid = models.IntegerField(blank=True, null=True)
    requestCurrencyCode = models.CharField(max_length=20, blank=True, null=True)
    requestDate = models.CharField(max_length=200, blank=True, null=True)
    payments = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Cellulant Webhook"
        verbose_name_plural = "Cellulant Webhook"

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