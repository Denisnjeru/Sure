from django.contrib import admin

from .models import *

# Register your models here.
@admin.register(Stk)
class StkAdmin(admin.ModelAdmin):
    list_display = [
        "amount",
        "mpesa_confirmation_code",
        "reference",
        "phone_number",
        "result_code",
        "result_desc"
    ]
    list_filter = [
        "result_desc"
    ]
    search_fields = [
        "phone_number",
        "mpesa_confirmation_code"
    ]

@admin.register(DpoToken)
class DpoTokenAdmin(admin.ModelAdmin):
    list_display = [
        "response_code",
        "explanation",
        "token",
        "reference"
    ]
    list_filter = [
        "response_code"
    ]
    search_fields = [
        "reference",
        "reference"
    ]

@admin.register(DpoPayment)
class DpoPaymentAdmin(admin.ModelAdmin):
    list_display = [
        "response_code",
        "customer_name",
        "reference",
        "payment_status",
    ]
    list_filter = [
        "payment_status"
    ]
    search_fields = [
        "reference",
    ]
