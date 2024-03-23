import json, base64, hashlib
import requests
import os
import xml.etree.ElementTree as ET

from django import http, apps
from django.shortcuts import redirect
from datetime import datetime, timedelta, date
from base64 import b64decode, b64encode
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from pathlib import Path
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from pprint import pprint
from requests.auth import HTTPBasicAuth
from decouple import config
from Crypto.Cipher import AES

from .models import *
from apps.core.utils import weasy_pdf
from apps.core.models import CategoryOrder
from apps.payments.utils import send_zero_charge_success_email, send_dpo_receipt_email
from apps.suppliers.serializers import EmptySerializer
from apps.payments.tasks import save_payment_receipt

# Create your views here.
@csrf_exempt
def MpesaAccessToken(request):
    """
    Function to generate token from the consumer secret and key
    """
    consumer_key = config('CONSUMER_KEY')
    consumer_secret = config('CONSUMER_SECRET')

    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    # r = requests.request("GET", api_URL, headers = { 'Authorization': f'Bearer {authorization}' })
    # print(r)

    auth = json.loads(r.text)
    token = auth['access_token']
    return token

@csrf_exempt
def STKPush(request,phone,amount,account_no):
    """
    Initiate stk push to client. Pass phone number of the client and amount to be billed as parameters.
    Will be called by any the other fucntion that requires to perform a billing and return the data response from safaricom
    """
    api_transaction_URL = 'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest'
    BusinessShortCode = 174379;
    LipaNaMpesaPasskey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919';

    try:
        access_token = MpesaAccessToken(request)
    except Exception as e:
        return 'error'

    data = None

    get_now = datetime.now()
    payment_time = get_now.strftime("%Y%m%d%H%M%S")
    to_encode = '{}{}{}'.format(
        BusinessShortCode, LipaNaMpesaPasskey, payment_time)
    payment_password = (b64encode(to_encode.encode('ascii'))).decode("utf-8")

    if access_token:
        headers = {"Authorization": "Bearer %s" % access_token}
        request = {
              "BusinessShortCode": BusinessShortCode,
              "Password": payment_password,
              "Timestamp": payment_time,
              "TransactionType": "CustomerPayBillOnline",
              "Amount": amount,
              "PartyA": phone,
              "PartyB": BusinessShortCode,
              "PhoneNumber": phone,
              "CallBackURL": config("SITE_URL") + '/api/v1/payments/stk_confirmation/',
              "AccountReference": account_no,
              "TransactionDesc": account_no
        }
        response = requests.post(
            api_transaction_URL, json=request, headers=headers)
        data = json.loads(response.text)

        MerchantRequestID = data.get('MerchantRequestID')
        CheckoutRequestID = data.get('CheckoutRequestID')

        stk = Stk.objects.create(merchant_request_id=MerchantRequestID,checkout_request_id=CheckoutRequestID, reference=account_no)
    else:
        print('access token failed')
    return data

class STKConfirmation(viewsets.GenericViewSet):
    """
    Method that is called back by safaricom in the case of an stk push
    """

    def get_serializer_class(self):
        return EmptySerializer

    def create(self, request, format=None):
        data = JSONParser().parse(request)
        get_data = data.get('Body').get('stkCallback')
        get_success_data = get_data.get('CallbackMetadata')
        pprint(data)
        if get_data:
            MerchantRequestID = get_data.get(
                'MerchantRequestID')
            CheckoutRequestID = get_data.get(
                'CheckoutRequestID')
            ResultCode = get_data.get('ResultCode')
            ResultDesc = get_data.get('ResultDesc')

            if get_success_data:
                get_items = get_success_data.get('Item')
                for i in get_items:
                    if i['Name'] == 'Amount':
                        Amount = i.get('Value')
                    elif i['Name'] == 'MpesaReceiptNumber':
                        MpesaReceiptNumber = i.get('Value')
                    elif i['Name'] == 'PhoneNumber':
                        PhoneNumber = i.get('Value')
                    elif i['Name'] == 'Balance':
                        Balance = i.get('Value')
                    elif i['Name'] == 'TransactionDate':
                        TransactionDate = i.get('Value')
                    else:
                        continue

            else:
                Amount = None
                MpesaReceiptNumber = None
                PhoneNumber = None
                Balance = None
                TransactionDate = None

            stk_response, created = Stk.objects.update_or_create(merchant_request_id=MerchantRequestID,checkout_request_id=CheckoutRequestID, \
                            defaults={
                                'merchant_request_id':MerchantRequestID,'checkout_request_id':CheckoutRequestID,
                                'result_code': ResultCode,'result_desc':ResultDesc,'amount':Amount,'mpesa_confirmation_code':MpesaReceiptNumber, \
                                'phone_number':PhoneNumber,'balance':Balance,'transaction_date':TransactionDate
                            })

            if ResultCode == 0:
                payment = apps.apps.get_model("core", "Payment").objects.create(
                    model='mpesa',
                    instance_id=stk_response.id,
                    timestamps=stk_response.transaction_date
                )
                category_orders = apps.apps.get_model("core", "CategoryOrder").objects.filter(code=stk_response.reference)
                category_orders.update(
                    payment_status=CategoryOrder.PAID,
                    payment_id=payment.id
                )

                categories = []
                total = 0
                for category_order in category_orders:
                    category = category_order.category
                    categories.append(category)
                    total += category.bid_charge

                supplier = apps.apps.get_model(
                    "suppliers", "Supplier").objects.filter(id=category_orders[0].supplier_id).first()

                send_mpesa_receipt_email(stk_response, supplier, categories)

        return Response({
            'success': 'Called successfully'

        }, status=status.HTTP_200_OK)


class MpesaC2BValidation(viewsets.GenericViewSet):
    def create(self, request, format=None):
        data = JSONParser().parse(request)

        print('MPESA TRANSACTION VALIDATION::::::::::::::::::::::::::::::')
        pprint(data)
        print('MPESA TRANSACTION VALIDATION::::::::::::::::::::::::::::::')

        return Response({
            'ResultCode': 0,
            'ResultDesc': 'Accepted'
        }, status=status.HTTP_200_OK)


class MpesaC2BConfirmation(viewsets.GenericViewSet):
    def create(self, request, format=None):
        data = JSONParser().parse(request)

        print('MPESA TRANSACTION CONFIRMATION::::::::::::::::::::::::::::::')
        pprint(data)
        print('MPESA TRANSACTION CONFIRMATION::::::::::::::::::::::::::::::')

        return Response({
            'ResultCode': 0,
            'ResultDesc': 'Accepted'
        }, status=status.HTTP_200_OK)

class MpesaSimulateC2B(viewsets.GenericViewSet):

    def list(self, request):
        simulate_c2b_URL = 'https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate'
        access_token = MpesaAccessToken(request)
        pprint(access_token)
        shortcode = settings.SHORTCODE

        if access_token:
            headers = {"Authorization": "Bearer %s" % access_token}

            data = {
                "ShortCode": shortcode,
                "CommandID": "CustomerBuyGoodsOnline",
                "Amount": "1",
                "Msisdn": "254708374149",
                "BillRefNumber": "Test payment on User"
            }

            response = requests.post(
                simulate_c2b_URL, json=data, headers=headers)

            pprint(response.text)

        return Response({
            "status": 'Done'
        }, status=status.HTTP_200_OK)

@csrf_exempt
def dpo_get_token(amount, currency, reference, supplier):
    url = "https://secure.3gdirectpay.com/API/v6/"

    print(config("DPO_COMPANY_TOKEN"))
    print(config("DPO_SERVICE_TYPE"))
    print(config("DPO_BACK_URL"))
    print(config("DPO_CALLBACK_URL"))
    print(amount)
    print(currency)
    print(reference)
    print(supplier.first_name)
    print(supplier.last_name)
    print(supplier.country)
    print(supplier.email)
    print(supplier.phone_number)
    print(supplier.address)
    print(datetime.now().strftime('%Y/%m/%d %H:%M'))

    body = (
        f'<?xml version="1.0" encoding="utf-8"?>'
        f"<API3G>"
        f'<CompanyToken>{config("DPO_COMPANY_TOKEN")}</CompanyToken>'
        f"<Request>createToken</Request>"
        f"<Transaction>"
        f"<PaymentAmount>{ amount }</PaymentAmount>"
        f"<PaymentCurrency>{ currency }</PaymentCurrency>"
        f"<CompanyRef>{ reference }</CompanyRef>"
        f"<CompanyAccRef>{ reference }</CompanyAccRef>"
        f'<RedirectURL>{config("DPO_CALLBACK_URL")}</RedirectURL>'
        f'<BackURL>{config("DPO_BACK_URL")}</BackURL>'
        f"<CompanyRefUnique>0</CompanyRefUnique>"
        f"<PTL>5</PTL>"
        f"<customerFirstName>{ supplier.first_name }</customerFirstName>"
        f"<customerLastName>{ supplier.last_name }</customerLastName>"
        f"<customerCity>{ supplier.country }</customerCity>"
        f"<customerEmail>{ supplier.email }</customerEmail>"
        f"<customerPhone>{ supplier.phone_number }</customerPhone>"
        f"<customerAddress>{ supplier.address }</customerAddress>"
        f"</Transaction>"
        f"<Services>"
        f"<Service>"
        f"<ServiceType>{config('DPO_SERVICE_TYPE')}</ServiceType>"
        f"<ServiceDescription>Payment for {reference}</ServiceDescription>"
        f"<ServiceDate>{ datetime.now().strftime('%Y/%m/%d %H:%M') }</ServiceDate>"
        f"</Service>"
        f"</Services>"
        f"</API3G>"
    )
    response = requests.post(url=url, data=body)
    print(response.text)

    root = ET.fromstring(response.text)
    response_code = root.find("Result").text
    if response_code == "000":
        token_element = root.find("TransToken")
        if token_element is not None:
            token = token_element.text
            DpoToken.objects.update_or_create(
                response_code=response_code,
                explanation=root.find("ResultExplanation").text,
                token=token,
                reference=root.find("TransRef").text,
            )
            return token
    else:
        DpoToken.objects.update_or_create(
            response_code=response_code,
            explanation=root.find("ResultExplanation").text,
            # reference=root.find('TransRef').text
        )
        return {"error": 'Payment request failed. Please try again!'}

def confirm_token(request, token):
    dpo_token = DpoToken.objects.filter(token=token).first()
    if dpo_token is not None:
        url = "https://secure.3gdirectpay.com/API/v6/"
        body = (
            f'<?xml version="1.0" encoding="utf-8"?>'
            f"<API3G>"
            f'<CompanyToken>{config("DPO_COMPANY_TOKEN")}</CompanyToken>'
            f"<Request>verifyToken</Request>"
            f"<TransactionToken>{dpo_token.token}</TransactionToken>"
            f"</API3G>"
        )

        response = requests.post(url=url, data=body)
        print(response.status_code)
        print(response.text)
        root = ET.fromstring(response.text)
        response_code = root.find("Result").text

        dpo_payment = DpoPayment.objects.create(
            response_code=response_code,
            explanation=root.find("ResultExplanation").text,
            customer_name=root.find("CustomerName").text,
            customer_credit=root.find("CustomerCredit").text,
            transaction_approval=root.find("TransactionApproval").text,
            transaction_currency=root.find("TransactionCurrency").text,
            transaction_amount=root.find("TransactionAmount").text,
            fraud_alert=root.find("FraudAlert").text,
            fraud_explanation=root.find("FraudExplnation").text,
            transaction_net_amount=root.find("TransactionNetAmount").text,
            transaction_settlement_date=root.find("TransactionSettlementDate").text,
            transaction_rolling_reverse_amount=root.find(
                "TransactionRollingReserveAmount"
            ).text,
            transaction_rolling_reverse_date=root.find(
                "TransactionRollingReserveDate"
            ).text,
            customer_phone=root.find("CustomerPhone").text,
            customer_country=root.find("CustomerCountry").text,
            customer_address=root.find("CustomerAddress").text,
            customer_city=root.find("CustomerCity").text,
            customer_zip=root.find("CustomerZip").text,
            mobile_payment_request=root.find("MobilePaymentRequest").text,
            reference=root.find("AccRef").text,
        )

        pending_orders = apps.apps.get_model("core", "CategoryOrder").objects.filter(
            code=root.find("AccRef").text,
            payment_status=CategoryOrder.PENDING,
        )

        if response_code == "000":
            amount = root.find("TransactionAmount").text
            reference = root.find("AccRef").text

            if pending_orders.count() > 0:
                categories = []
                pending_orders_total = 0
                for category_order in pending_orders:
                    category = category_order.category
                    categories.append(category)
                    pending_orders_total += category.bid_charge

                if float(amount) == float(pending_orders_total):
                    dpo_payment.payment_status = DpoPayment.COMPLETED
                    dpo_payment.save()

                    payment = apps.apps.get_model("core", "Payment").objects.create(
                        model="DpoPayment",
                        instance_id=dpo_payment.id,
                        timestamps=f"{datetime.now()}",
                    )

                    pending_orders.update(
                        payment_status=CategoryOrder.PAID, payment_id=payment.id
                    )

                    supplier = apps.apps.get_model(
                        "suppliers", "Supplier").objects.filter(id=pending_orders[0].supplier_id).first()

                    send_dpo_receipt_email(supplier=supplier, dpo_payment=dpo_payment)
                    messages.success(request, "Payment processed successfully")
                    context = {
                        "succcess": 'Payment processed successfully.'
                    }
                    return context
                else:
                    context = {
                        "error": 'Payment did not match the pending orders.'
                    }
                    return context
            else:
                dpo_payment.payment_status = DpoPayment.PROCESSING
                dpo_payment.save()

                pending_orders.update(
                    payment_status=CategoryOrder.PROCESSING,
                )
                context = {
                    "error": 'There are no pending orders in your cart.'
                }
                return context
        elif response_code == "002" or response_code == "007" or response_code == "003":
            dpo_payment.payment_status = DpoPayment.PROCESSING
            dpo_payment.save()

            pending_orders.update(
                payment_status=CategoryOrder.PROCESSING,
            )
            context = {
                "error": 'There was an error processing your payment. Kindly Contact Us.'
            }
            return context
        else:
            dpo_payment.payment_status = DpoPayment.PROCESSING
            dpo_payment.save()
            context = {
                "error": 'There was an error processing your payment. Kindly Contact Us.'
            }
            return context
    else:
        context = {
            "error": 'Payment request failed. Reference provided does not match any orders. Please try again!'
        }
        return context

class DPOConfirmationView(viewsets.GenericViewSet):
    """
    Method that is called back by DPO for payment confirmation
    """

    def get_serializer_class(self):
        return EmptySerializer

    def create(self, request, format=None):
        transaction_id = request.GET.get("TransID", None)
        ccd_approval = request.GET.get("CCDapproval", None)
        transaction_token = request.GET.get("TransactionToken", None)
        reference = request.GET.get("CompanyRef")

        DpoTokenCallBack.objects.create(
            transaction_id=transaction_id,
            ccd_approval=ccd_approval,
            transaction_token=transaction_token,
            reference=reference,
        )

        confirmed = confirm_token(request, transaction_token)

        return redirect("http://localhost:8080/")


@csrf_exempt
def cellulant_payment(payload):

    IV_key = config("CellulantIVKey")
    secret_key = config("CellulantSecretKey")

    algorithm = AES.MODE_CBC

    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

    secret = hashlib.sha256(secret_key.encode()).hexdigest()[:32]
    IV = hashlib.sha256(IV_key.encode()).hexdigest()[:16]

    cipher = AES.new(secret.encode("utf-8"), algorithm, IV.encode("utf-8"))
    crypt = cipher.encrypt(pad(json.dumps(payload)).encode())



    data = {
        "params": base64.b64encode(base64.b64encode(crypt)).decode("utf-8"),
        "countryCode": payload["countryCode"],
    }

    return data

class CellulantWebhookView(viewsets.GenericViewSet):
    """
    Method that is called back by Cellulant for payment confirmation
    """

    def create(self, request, format=None):

        body_unicode = request.body.decode("utf-8")
        data = json.loads(body_unicode)
        total = 0
        payment = CellulantPayment(
            accountNumber=data["accountNumber"],
            currencyCode=data["originalRequestCurrencyCode"],
            checkoutRequestID=data["checkoutRequestID"],
            requestAmount=data["requestAmount"],
            amountPaid=data["amountPaid"],
            merchantTransactionID=data["accountNumber"],
            requestDate=data["requestDate"],
            requestStatusDescription=data["requestStatusDescription"],
            MSISDN=data["MSISDN"],
        )
        payment.save()

        payment_model = apps.apps.get_model("core", "Payment").objects.create(
            model="CellulantPayment",
            instance_id=payment.id,
            timestamps=datetime.datetime.now(),
        )

        checkoutRequestID = data["checkoutRequestID"]
        merchantTransactionID = data["accountNumber"]

        cellulant_response = CellulantWebhook.objects.create(
            checkoutRequestID=checkoutRequestID,
            merchantTransactionID=merchantTransactionID,
            requestStatusCode=data["requestStatusCode"],
            requestAmount=data["requestAmount"],
            requestStatusDescription=data["requestStatusDescription"],
            MSISDN=data["MSISDN"],
            serviceCode=data["serviceCode"],
            accountNumber=data["accountNumber"],
            currencyCode=data["currencyCode"],
            amountPaid=data["amountPaid"],
            requestCurrencyCode=data["requestCurrencyCode"],
            requestDate=data["requestDate"],
            payments=data["payments"],
        )

        if cellulant_response.requestStatusCode == 178:
            statusCode = 183
        else:
            statusCode = 180

        payload = {
            "checkoutRequestID": checkoutRequestID,
            "merchantTransactionID": merchantTransactionID,
            "statusCode": statusCode,
            "statusDescription": "Payment was processed successfully",
            "receiptNumber": data["accountNumber"],
        }

        return JsonResponse(dict(payload))

class CellulantSuccessView(viewsets.GenericViewSet):
    """
    Method that is called back by Cellulant on successful payment
    """

    def create(self, request, format=None):

        print(request.POST)

        return Response(status=status.HTTP_200_OK)

class CellulantPendingView(viewsets.GenericViewSet):
    """
    Method that is called back by Cellulant on successful payment
    """

    def create(self, request, format=None):

        print(request.POST)

        return Response(status=status.HTTP_200_OK)

class CellulantFailView(viewsets.GenericViewSet):
    """
    Method that is called back by Cellulant on successful payment
    """

    def create(self, request, format=None):

        print(request.POST)

        return Response(status=status.HTTP_200_OK)

@csrf_exempt
def make_zero_charge(category_orders):

    total = 0
    payment_ref = None
    categories = []
    for category_order in category_orders:
        payment_ref = category_order.code
        total += category_order.category.bid_charge

    if total == 0:
        for category_order in category_orders:
            if category_order.category.bid_charge == 0:
                category_order.payment_status=1
                category_order.save()
                categories.append(category_order.category)

    supplier = apps.apps.get_model(
                    "suppliers", "Supplier").objects.filter(id=category_orders[0].supplier_id).first()

    send_zero_charge_success_email(supplier=supplier, categories=categories, payment_ref=payment_ref)

    data = {
        'payment_ref': payment_ref,
    }

    return data
