import datetime
import threading
from django.core.mail import EmailMessage

from django.conf import settings
from decouple import config


def get_my_current_site():
    if settings.DEBUG:
        current_site_url = config("DEV_SITE_URL")
    else:
        current_site_url = config("PROD_SITE_URL")
    
    return current_site_url


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()


def send_email(data):
    email = EmailMessage(
        subject=data["email_subject"],
        body=data["email_body"],
        to=[data["to_email"]],
    )
    EmailThread(email).start()


def check_leapyear(year):
    rem = year % 4
    if rem == 0:
        return True
    else:
        return False


def OneYear(year, month, day):
    if check_leapyear(int(year) + 1) or check_leapyear(int(year)):
        if (int(month) == 2) and int(day) == 29:
            return datetime.date(int(year) + 1, int(month), int(1))
        else:
            return datetime.date(int(year) + 1, int(month), int(day))
    else:
        return datetime.date(int(year) + 1, int(month), int(day))


def get_local_filepath(file_url):
    media_root = settings.MEDIA_ROOT
    nw_media_root = media_root.split("/")[:-1]
    nw_url = "/".join(nw_media_root)
    return nw_url + file_url

def timezone_aware_time():
    utc = datetime.timezone(datetime.timedelta(hours=+3))
    time = datetime.datetime.now().replace(tzinfo=utc)

    return time
