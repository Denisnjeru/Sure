import re

import requests
from celery import shared_task
from django import apps
from django.http import JsonResponse
from sentry_sdk import capture_exception

from apps.core.models import HelpContact
from apps.prequal.email_notifications import calculate_potential_suppliers


class SMS:
    """Sends all sms's for the system"""

    def __init__(self):
        # set to  store phone_numbers
        self.phone_numbers = set()
        self.count = 0

    def validate_phone(self, phone_number, country=None):
        """
        Validates  the phone number
        """
        # The regualr expression matches the string  given (r'^([0-9]{3})[7]\d{8}$', '2547xxxxxxxx')
        # Should check also if its starts with 0 and add 254 or the  countries calling_code removing 0
        # Uses  the following reg to match the number
        # (r'^[0]\d{9}$', '01159127987')
        # for removing spaces in the number -- >> re.sub(r"\s+", "", s)
        if country == None or country == "Kenya":
            reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
            reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
            reg2 = re.compile(r"^[0]\d{9}$")
            reg3 = re.compile(r"^[7]\d{8}$")
            phone_number = re.sub(r"\s+", "", phone_number)
            if reg.search(phone_number):
                return phone_number
            elif reg1.search(phone_number):
                phone_number = phone_number.replace("+", "")
                return phone_number
            elif reg2.search(phone_number):
                phone_number = re.sub(phone_number[0], "254", phone_number, 1)
                return phone_number
            elif reg3.search(phone_number):
                phone_number = "254" + phone_number[:9]
                return phone_number
            else:
                return False
        else:
            help_contacts = HelpContact.objects.get(country=country)
            calling_code = help_contacts.country_calling_code
            reg = re.compile(r"^([0-9]{3})[7]\d{8}$")
            reg1 = re.compile(r"^(\+)([0-9]{3})[7]\d{8}$")
            reg2 = re.compile(r"^[0]\d{9}$")
            reg3 = re.compile(r"^[7]\d{8}$")
            phone_number = re.sub(r"\s+", "", phone_number)
            try:
                if reg.search(phone_number):
                    return phone_number
                elif reg1.search(phone_number):
                    phone_number = phone_number.replace("+", "")
                    return phone_number
                elif reg2.search(phone_number):
                    phone_number = re.sub(
                        phone_number[0], calling_code, phone_number, 1
                    )
                    return phone_number
                elif reg3.search(phone_number):
                    phone_number = calling_code + phone_number[:9]
                    return phone_number
                else:
                    return False
            except Exception as e:
                print(f"Error validating phone number: {e}")

    """
    phone_number in phone_numbers
    lambda: phone_number in  phone_numbers
    """

    def send_sms_default(self, phone_number, category):
        # if it starts acting up uncomment the inactive password and comment the active password
        api_url = "http://52.15.88.116/bulkAPIV2/"
        country = category.prequalification.company.country
        valid_phone_number = self.validate_phone(phone_number, country)
        if valid_phone_number:
            if valid_phone_number not in self.phone_numbers:
                try:

                    request_sms = {
                        "user": "Emmanuel.Gathage",
                        # "pass": "c6caa8d1a84c0a7d3d45dac2956e78311e08ecc4",
                        "pass": "d2car45t64c9ertd3d45wsad2956e564774e08ecc4",
                        "message": f"Tendersure is managing the prequalification for "
                                   f"{category.prequalification.company.company_name}"
                                   f". Closing date {category.closing_date.date()}. To bid go to www.tendersure.co.ke and "
                                   f"click 'Available Jobs'",
                        "msisdn": valid_phone_number,
                        "shortCode": "TENDERSURE",
                        # "messageID": f"{ category.name }" + f"{ self.count }",
                        "coding": "utf-8",
                    }
                    self.count += 1
                    response = requests.get(api_url, params=request_sms)
                    self.phone_numbers.add(valid_phone_number)
                    print(request_sms)
                    print(f"count: {self.count}")
                except Exception as e:
                    print(f"Error sending sms: {e}")
            else:
                print(f"Sms already sent to: {valid_phone_number}")
        else:
            print(f"Not a valid phone number!")


def sms_category_notifications(data, category_id):
    to = data["to"]
    category = apps.apps.get_model('prequal', 'Category').objects.get(id=category_id)

    messages = []
    potential_suppliers = None

    sms = SMS()
    if to == "potentialsms":
        # message = data["content"]
        type = data["type"]
        category_type = category.category_type
        # calculate potential suppliers
        if category.paid_bidders:
            potential_suppliers = calculate_potential_suppliers(
                category.paid_bidders, category
            )
        elif len(category.paid_bidders) == 0:
            category_type_suppliers = []
            potential_dictionary = {}
            potential_dictionary = category_type.suppliers_list(
                category.job.company.country
            )
            category_type_suppliers.extend(
                potential_dictionary["registered_suppliers"]
            )
            category_type_suppliers.extend(potential_dictionary["old_suppliers"])
            potential_suppliers = category_type_suppliers

        try:
            if potential_suppliers:
                if type == "Customsms":
                    for potential_supplier in potential_suppliers:
                        if potential_supplier._meta.model.__name__ == "CategoryTypeSupplier":
                            pass
                        else:
                            pass
                elif type == "Defaultsms":
                    print('got here')
                    for potential_supplier in potential_suppliers:
                        if potential_supplier:
                            if potential_supplier._meta.model.__name__ == "CategoryTypeSupplier":
                                supplier_phone = potential_supplier.primary_phone
                                sms.send_sms_default(supplier_phone, category)
                            else:
                                supplier_phone = potential_supplier.phone_number
                                sms.send_sms_default(supplier_phone, category)
            messages.append("Sms Notifications sent successfully!")
            context = {
                "messages": messages
            }
            return context
        except Exception as e:
            messages.append("Sms Notifications were not sent!")
            capture_exception(e)
            context = {
                "messages": messages,
                "error": e
            }
            print(e)
            return context

    elif to == "responsivesms":
        """
        Send SMS to responsive bidders
        """
        try:
            message = data["content"]
            # type = data["type"]
            responsive_bidders = category.responsive_bidders
            for responsive_bidder in responsive_bidders:
                supplier_phone = responsive_bidder.phone_number
                send_supplier_sms.delay(message, supplier_phone)
            messages.append("Sms Notification sent successfully")
            context = {
                "messages": messages
            }
            return context

        except Exception as e:
            messages.append("Sms Notifications were not sent!")
            capture_exception(e)
            context = {
                "messages": messages,
                "errors": e
            }
            return context

    elif to == "non-responsivesms":
        """
        Send to non-responsive bidders
        """
        try:
            message = data["content"]
            # type = data["type"]
            non_responsive_bidders = category.non_responsive_bidders
            print(non_responsive_bidders)
            for non_responsive_bidder in non_responsive_bidders:
                supplier_phone = non_responsive_bidder.phone_number
                send_supplier_sms.delay(message, supplier_phone)
            messages.append("Sms Notification sent successfully")
            context = {
                "messages": messages,
            }
            return context

        except Exception as e:
            messages.append("Sms Notifications were not sent!")
            capture_exception(e)
            context = {
                "messages": messages
            }
            return context


@shared_task(bind=True)
def send_supplier_sms(self, message=None, phone_number=None):
    """
    Send supplier sms
    """
    sms = SMS()
    SMS_API_URL = "http://52.15.88.116/bulkAPIV2/"

    if message is not None and phone_number is not None:
        if phone_number is not None:
            valid_phone_number = sms.validate_phone(phone_number, country=None)
            params = {
                "user": "Emmanuel.Gathage",
                "pass": "d2car45t64c9ertd3d45wsad2956e564774e08ecc4",
                "message": message, "msisdn": valid_phone_number,
                "shortCode": "TENDERSURE", "coding": "utf-8",
            }
            try:
                response = requests.get(SMS_API_URL, params=params).text
                print(response)
                return response
            except Exception as e:
                capture_exception(e)
                print(e)
        else:
            return JsonResponse({"message": "Ivalid phone number"})
    else:
        return JsonResponse({"message": "Phone Number is None"})
