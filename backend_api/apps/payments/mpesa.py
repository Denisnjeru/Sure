import base64
import json
import re
from datetime import datetime

import requests
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from requests.auth import HTTPBasicAuth
from sentry_sdk import capture_exception


def get_mpesa_access_token():
    consumer_key = ""
    consumer_secret = ""
    api_URL = (
        "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    )

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token["access_token"]
    return validated_mpesa_access_token


class LipaNaMpesaPassword:
    lipa_time = datetime.now().strftime("%Y%m%d%H%M%S")
    Business_short_code = ""
    passkey = ""

    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode("utf-8")


@csrf_exempt
def register_urls(request):
    access_token = get_mpesa_access_token()
    # print(access_token)
    # api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    api_url = "https://api.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {
        "ShortCode": "379127",
        "ResponseType": "Completed",
        "ConfirmationURL": "https://www.e.tendersure.co.ke/api/v1/c2b/confirmation",
        "ValidationURL": "https://www.e.tendersure.co.ke/api/v1/c2b/validation",
    }
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def lipa_na_mpesa_online(request):

    phone_number = request.POST["PhoneNumber"]
    phone_number_validates = re.findall("^254", phone_number)
    actual_phone_number = f"{254}{phone_number[-9:]}"
    lipa_time = datetime.now().strftime("%Y%m%d%H%M%S")
    Business_short_code = "379127"
    passkey = "b1faca372d47283385676397611bcc6707f769568463a8bc91c126105afeb9f6"
    data_to_encode = Business_short_code + passkey + lipa_time
    online_password = base64.b64encode(data_to_encode.encode())
    decode_password = online_password.decode("utf-8")

    if phone_number_validates:
        access_token = get_mpesa_access_token()
        amount = request.POST["Amount"]
        print(amount)
        print(request.POST["PhoneNumber"])
        print(request.POST["AccountReference"])
        api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        headers = {"Authorization": "Bearer %s" % access_token}
        request_mpesa = {
            "BusinessShortCode": "379127",
            "Password": decode_password,
            "Timestamp": lipa_time,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": float(amount),
            "PartyA": actual_phone_number,
            "PartyB": "379127",
            "PhoneNumber": actual_phone_number,
            "CallBackURL": "https://www.e.tendersure.co.ke/api/v1/c2b/validation",
            "AccountReference": str(request.POST["AccountReference"]),
            "TransactionDesc": "You are about to pay ",
        }

        response = requests.post(api_url, json=request_mpesa, headers=headers)
        print(response.text)
        # messages.success(
        #     request,
        #     "We have sent the Mpesa payment details to your phone number. Proceed to make payment by putting you Mpesa pin",
        # )
        return redirect("Supplier:instructions")
    else:
        # messages.error(
        #     request,
        #     "Invalid phone number format, make sure phone number start with 254",
        # )
        return redirect("Supplier:mpesa_payment")


# @csrf_exempt
# def validation(request):
#
#     context = {"ResultCode": 0, "ResultDesc": "Accepted"}
#
#     print(MpesaPayment.__name__)
#     return JsonResponse(dict(context))


# @csrf_exempt
# def confirmation(request):
#     mpesa_body = request.body.decode("utf-8")
#     mpesa_payment = json.loads(mpesa_body)
#     print(mpesa_payment)
#     json_dump = json.dumps(mpesa_payment)
#     countries = ["Uganda", "Malawi"]
#     payment = MpesaPayment(
#         first_name=mpesa_payment["FirstName"],
#         last_name=mpesa_payment["LastName"],
#         description=mpesa_payment["TransID"],
#         phone_number=mpesa_payment["MSISDN"],
#         amount=mpesa_payment["TransAmount"],
#         reference=mpesa_payment["BillRefNumber"],
#         email="eprocure@qedsolutions.co.ke",
#         type=mpesa_payment["TransactionType"],
#         payment_status=MpesaPayment.COMPLETED,
#     )
#     payment.save()
#
#     payment_model = Payment(
#         model="MpesaPayment", instance_id=payment.id, timestamps=datetime.datetime.now()
#     )
#     payment_model.save()
#
#     try:
#         # total = 0
#         # orders = CategoryOrder.objects.filter(code=mpesa_payment['BillRefNumber'])
#         # for category_order in orders:
#         #     total += category_order.category.bid_charge
#         #
#         # if total > mpesa_payment['TransAmount']:
#         #     print('Amount insufficient')
#         #     context = {
#         #         "ResultCode": 0,
#         #         "ResultDesc": "Accepted"
#         #     }
#         #     return JsonResponse(dict(context))
#         BillRefNumber = mpesa_payment["BillRefNumber"]
#         if BillRefNumber == "" or BillRefNumber == None:
#             context = {"ResultCode": 0, "ResultDesc": "Accepted"}
#             return JsonResponse(dict(context))
#
#         BillRefNumber = BillRefNumber.upper()
#         pending_orders = CategoryOrder.objects.filter(
#             code=BillRefNumber, payment_status=CategoryOrder.PENDING
#         )
#         total = 0
#         for order in pending_orders:
#             if order.category:
#                 total += float(order.category.bid_charge)
#             elif order.asset_disposal_category:
#                 total += order.asset_disposal_category.bid_charge
#
#         if total != float(mpesa_payment["TransAmount"]):
#             context = {"ResultCode": 0, "ResultDesc": "Accepted"}
#             return JsonResponse(dict(context))
#         elif total == float(mpesa_payment["TransAmount"]):
#
#             orders = pending_orders
#             categories = []
#             # total = 0
#             for category_order in orders:
#                 category_order.payment_status = CategoryOrder.PAID
#                 category_order.payment = payment_model
#                 category_order.save()
#
#                 if category_order.category:
#                     categories.append(category_order.category)
#                     # total += category_order.category.bid_charge
#                 elif category_order.asset_disposal_category:
#                     categories.append(category_order.asset_disposal_category)
#                     # total += category_order.asset_disposal_category.bid_charge
#
#             supplier = SupplierProfile.objects.get(
#                 id=orders.first().supplier_profile.id
#             ).supplier
#             user = User.objects.filter(id=supplier.user_ptr_id)
#
#             if category_order.category:
#                 CompanySupplier.objects.update_or_create(
#                     supplier_id=supplier.id,
#                     company_id=category_order.category.job.company_id,
#                 )
#             elif category_order.asset_disposal_category:
#                 CompanySupplier.objects.update_or_create(
#                     supplier_id=supplier.id,
#                     company_id=category_order.asset_disposal_category.asset_disposal.company_id,
#                 )
#
#             amount = mpesa_payment["TransAmount"]
#
#             """ Send Payment Acknowledgement"""
#             time = datetime.datetime.now()
#             file_path = "media/payment_receipts/%s" % supplier.company_name.replace(
#                 " ", "_"
#             ).replace("/", "_")
#
#             filename = "%s_%d_%d.pdf" % (
#                 supplier.company_name.replace(" ", "_").replace("/", "_"),
#                 time.year,
#                 time.month,
#             )
#
#             Path(file_path).mkdir(parents=True, exist_ok=True)
#             template_path = os.path.join(
#                 BASE_DIR + "/mpesa_api/templates/receipts/new_receipt2.html"
#             )
#             # supplier = supplier.company_name.replace("/", "_")
#
#             od = orders.first()
#             if od.category:
#                 currency = od.category.currency
#                 job = od.category.job
#             elif od.asset_disposal_category:
#                 currency = od.asset_disposal_category.currency
#                 job = od.asset_disposal_category.asset_disposal
#
#             context = {
#                 "user": user,
#                 "payment_model": payment_model,
#                 "supplier": supplier,
#                 "payment": payment,
#                 "total": amount,
#                 "currency": currency,
#                 "name": f"{mpesa_payment['FirstName']} {mpesa_payment['LastName']}",
#                 "phone_number": mpesa_payment["MSISDN"],
#                 "company_name": supplier.company_name,
#                 "job": job,
#                 "categories": categories,
#                 "date": datetime.datetime.now(),
#             }
#
#             pdf_file_path = weasy_pdf(
#                 template_src=template_path,
#                 context_dict=context,
#                 file_name=filename,
#                 file_path=file_path,
#             )
#
#             try:
#                 mode_of_payment = ("MPESA",)
#                 save_receipt = save_payment_receipt.delay(
#                     filepath=pdf_file_path,
#                     filename=filename,
#                     supplier_id=supplier.id,
#                     mode_of_payment=mode_of_payment,
#                     reference=mpesa_payment["BillRefNumber"],
#                     amount=amount,
#                     payment_date=datetime.datetime.now(),
#                 )
#             except Exception as e:
#                 capture_exception(e)
#
#             email_subject = "Acknowledging of Mpesa Payment"
#
#             body = render_to_string(
#                 "qed_users/payment_email.html",
#                 {
#                     "supplier": supplier,
#                     "order_number": mpesa_payment["BillRefNumber"],
#                     "paid_amount": amount,
#                     "categories": categories,
#                     "total": total,
#                     "mode_of_payment": "Mpesa",
#                     "currency": currency,
#                 },
#             )
#
#             message = render_to_string(
#                 "qed_users/payment_email.html",
#                 {
#                     "supplier": supplier,
#                     "order_number": mpesa_payment["BillRefNumber"],
#                     "paid_amount": amount,
#                     "categories": categories,
#                     "total": total,
#                     "mode_of_payment": "Mpesa",
#                     "currency": currency,
#                 },
#             )
#
#             email = EmailMultiAlternatives(
#                 subject=email_subject, body=body, to=[supplier.email]
#             )
#             email.attach_alternative(message, "text/html")
#             email.attach_file(pdf_file_path)
#             email.send(fail_silently=True)
#     except:
#         raise
#         pass
#
#     context = {"ResultCode": 0, "ResultDesc": "Accepted"}
#     return JsonResponse(dict(context))
