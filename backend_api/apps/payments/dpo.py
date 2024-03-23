def dpo_token_payload(request):
    supplier = Supplier.objects.get(user_ptr_id=request.user.id)
    supplier_orders = []
    basket_total = 0

    order1 = CategoryOrder.objects.filter(
        Q(category__status_open=True) | Q(asset_disposal_category__status_open=True),
        payment_status=CategoryOrder.PENDING,
        supplier_profile__supplier=supplier,
    ).first()

    if order1 is not None:
        if len(order1.code) == 0:
            payment_ref = CategoryOrder.generate_code(CategoryOrder())
        else:
            payment_ref = order1.code

        pending_orders = CategoryOrder.objects.filter(
            Q(category__status_open=True)
            | Q(asset_disposal_category__status_open=True),
            payment_status=CategoryOrder.PENDING,
            supplier_profile__supplier=supplier,
        )

        for order in pending_orders:
            if order.category:
                basket_total += order.category.bid_charge
            elif order.asset_disposal_category:
                basket_total += order.asset_disposal_category.bid_charge

            supplier_orders.append(order)

            if len(order.code) == 0:
                order.code = payment_ref
                order.save()
            payment_ref = order.code
        basket_amount = basket_total

        if order1.category:
            if order1.category.currency == "USH":
                currency = "UGX"
            if order1.category.currency == "TSH":
                currency = "TZS"
        elif order1.asset_disposal_category:
            if order1.asset_disposal_category.currency == "USH":
                currency = "UGX"
            if order1.asset_disposal_category.currency == "TSH":
                currency = "TZS"

        token = get_token(
            amount=int(float(basket_amount)),
            currency=currency,
            reference=payment_ref,
            supplier=supplier,
            request=request,
        )
        return token
    messages.error(request, "You have no pending orders in your cart")
    return redirect("Supplier:job_basket")


def get_token(amount, currency, reference, supplier, request):
    url = "https://secure.3gdirectpay.com/API/v6/"

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
        f"<ServiceDate>{ datetime.datetime.now().strftime('%Y/%m/%d %H:%M') }</ServiceDate>"
        f"</Service>"
        f"</Services>"
        f"</API3G>"
    )
    # f'<ServiceDescription>Bid Fee</ServiceDescription>' \
    # datetime.datetime.now().strftime("Y/m/d H:M")
    # 44481
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
        messages.error(request, "Payment request failed. Please try again!")
        return redirect("Supplier:job_basket")


@csrf_exempt
def confirmation(request):
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

    # context = {
    #     'transaction_id': transaction_id,
    #     'approval': ccd_approval,
    #     'transaction_token': transaction_token,
    #     'reference': reference
    # }
    confirmed = confirm_token(request, transaction_token)

    return confirmed


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

        pending_orders = CategoryOrder.objects.filter(
            Q(category__status_open=True)
            | Q(asset_disposal_category__status_open=True),
            payment_status=CategoryOrder.PENDING,
            code=root.find("AccRef").text,
        )

        if response_code == "000":
            amount = root.find("TransactionAmount").text
            reference = root.find("AccRef").text

            if pending_orders.count() > 0:
                pending_orders_total = pending_orders.aggregate(
                    total=Sum("category__bid_charge")
                )["total"]
                if float(amount) == float(pending_orders_total):
                    dpo_payment.payment_status = DpoPayment.COMPLETED
                    dpo_payment.save()

                    payment = Payment.objects.create(
                        model="DpoPayment",
                        instance_id=dpo_payment.id,
                        timestamps=f"{datetime.datetime.now()}",
                    )

                    pending_orders.update(
                        payment_status=CategoryOrder.PAID, payment_id=payment.id
                    )
                    supplier = Supplier.objects.filter(
                        user_ptr_id=request.user.id
                    ).first()
                    send_receipt(supplier=supplier, dpo_payment=dpo_payment)
                    messages.success(request, "Payment processed successfully")
                    return redirect("Supplier:successful_orders", reference)
                else:
                    messages.error(request, "Payment did not match the pending orders")
                    return redirect("Supplier:job_basket")
            else:
                dpo_payment.payment_status = DpoPayment.PROCESSING
                dpo_payment.save()

                pending_orders.update(
                    payment_status=CategoryOrder.PROCESSING,
                )
                messages.error(request, "There are no pending orders in your cart")
                return redirect("Supplier:job_basket")
        elif response_code == "002" or response_code == "007" or response_code == "003":
            dpo_payment.payment_status = DpoPayment.PROCESSING
            dpo_payment.save()

            pending_orders.update(
                payment_status=CategoryOrder.PROCESSING,
            )

            messages.error(
                request,
                "There was an error processing your payment. Kindly Contact Us: ",
            )
            return redirect("Supplier:job_basket")
        else:
            dpo_payment.payment_status = DpoPayment.PROCESSING
            dpo_payment.save()
            messages.error(
                request,
                "There was an error processing your payment. Kindly Contact Us: ",
            )
            return redirect("Supplier:job_basket")
    else:
        messages.error(
            request,
            "Payment request failed. Reference provided does not match any orders. Please try again!",
        )
        return redirect("Supplier:job_basket")


def send_receipt(supplier, dpo_payment):
    name = dpo_payment.customer_name
    phone_number = dpo_payment.customer_phone
    amount = dpo_payment.transaction_amount
    reference = dpo_payment.reference

    orders = CategoryOrder.objects.filter(
        Q(category__status_open=True) | Q(asset_disposal_category__status_open=True),
        code=reference,
    )
    currency = orders.first().category.currency
    time = datetime.datetime.now()
    file_path = "media/payment_receipts/%s" % supplier.company_name.replace(" ", "_")
    filename = "%s_%d_%d.pdf" % (
        supplier.company_name.replace(" ", "_"),
        time.year,
        time.month,
    )
    Path(file_path).mkdir(parents=True, exist_ok=True)

    template_path = os.path.join(
        BASE_DIR + "/payment_api/templates/payment_api/dpo/receipt.html"
    )

    user = User.objects.filter(id=supplier.user_ptr_id)
    categories = Category.objects.filter(
        id__in=orders.only("category_id").values("category_id")
    )

    context = {
        "user": user,
        "payment": dpo_payment,
        "total": amount,
        "name": f"{name}",
        "phone_number": phone_number,
        "company_name": supplier.company_name,
        "categories": categories,
        "date": datetime.datetime.now(),
    }

    pdf_file_path = weasy_pdf(
        template_src=template_path,
        context_dict=context,
        file_name=filename,
        file_path=file_path,
    )

    try:
        mode_of_payment = "DPO"
        save_receipt = save_payment_receipt.delay(
            filepath=pdf_file_path,
            filename=filename,
            supplier_id=supplier.id,
            mode_of_payment=mode_of_payment,
            reference=reference,
            amount=amount,
            payment_date=datetime.datetime.now(),
        )
    except Exception as e:
        capture_exception(e)

    email_subject = "Acknowledging of Payment"
    amount = amount
    body = render_to_string(
        "payment_api/dpo/email.html",
        {
            "supplier": supplier,
            "order_number": reference,
            "paid_amount": amount,
            "categories": categories,
            "total": amount,
            "currency": currency,
        },
    )

    message = render_to_string(
        "payment_api/dpo/email.html",
        {
            "supplier": supplier,
            "order_number": reference,
            "paid_amount": amount,
            "categories": categories,
            "total": amount,
            "currency": currency,
        },
    )

    email = EmailMultiAlternatives(
        subject=email_subject, body=body, to=[supplier.email]
    )
    email.attach_alternative(message, "text/html")
    email.attach_file(pdf_file_path)
    email.send()
    return True
