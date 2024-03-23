import datetime
from multiprocessing import context
import os
from pathlib import Path
from celery import shared_task
from django.apps import apps
from django.template.loader import render_to_string
from django.core.mail import (
    EmailMultiAlternatives,
    EmailMessage,
    get_connection,
    message,
)
import requests
from apps.common.utils import get_local_filepath

from .models import Auction, AuctionInvitee, AuctionTotalItemResponse


@shared_task(bind=True)
def send_participation_acknowledgment(self,supplier_id, auction_id, created=False):
    """
    Send the supplier email, to acknowledge submission of Auction
    :param supplier_id:
    :param categrory_id:
    :return:
    """
    auction = Auction.objects.filter(id=auction_id).first()
    supplier = (
        apps.get_model("suppliers", "Supplier").objects.filter(id=supplier_id).first()
    )

    if auction is not None and supplier is not None:
        try:
            email_subject = (
                "Tendersure: Auction Participation: %s " % auction.name.title()
            )
            if created:
                body = render_to_string(
                    "emails/auction_participation_acknowledgment.html",
                    {
                        "auction": auction,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )
            else:
                body = render_to_string(
                    "emails/rfq_response_update.html",
                    {
                        "category": auction,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )

            email = EmailMultiAlternatives(
                subject=email_subject, body=body, to=[supplier.email_address]
            )
            email.attach_alternative(body, "text/html")
            email.send()
            print(f"email send successfuly to {supplier.email_address}")

            context = {"success": "email sent successfuly"}
            return context
        except Exception as e:
            print(e)
            #cature exception
    else:
        context = {"error": "Auction or Supplier is None"}
        return context


@shared_task(bind=True)
def send_bid_responses(self,auction_id):
    """
    Sends the supplier PDF response of their Auction submission
    :param auction_id:
    "param supplier_id:
    :return:
    """
    try:
        auction = Auction.objects.filter(id=auction_id).first()
        suppliers = auction.participants["participants"]

        for supplier in suppliers:
            if supplier is not None and auction is not None:
                auction_response = AuctionTotalItemResponse.objects.filter(
                    supplier=supplier, auction=auction
                ).first()

                email_subject = "Tendersure: Your Auction Participation Responses: %s " % auction.name

                body = render_to_string(
                    "emails/rfq_responses_body.html",
                    {
                        "auction": auction,
                        "supplier": supplier,
                        "buyer_name": "Tendersure Team",
                        "buyer_logo": "tendersure_logo",
                    },
                )

                if auction_response.excel_url:
                    time = datetime.datetime.now()
                    filepath = get_local_filepath(auction_response.excel_url.url)
                    print(filepath)
                    email = EmailMultiAlternatives(
                        subject=email_subject, body=body, to=[supplier.email_address]
                    )
                    email.attach_alternative(body, "text/html")
                    email.attach_file(filepath)
                    email.send()
                    context = {"success": "email sent successfuly"}
                    return context
                else:
                    context = {"error": "No responses"}
                    return context

    except Exception as e:
        print(e)
        context = {"error": "Invalid email address"}
        return context


