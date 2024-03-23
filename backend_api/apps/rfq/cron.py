import datetime
import pytz

from apps.rfq.models import Category


def open_close_rfq():
    """
    Add to cron job to open and close RFQ categories automatically
    """
    
    time_utc = datetime.datetime.now(datetime.timezone.utc)

    open_categories = Category.objects.filter(closing_date__gte=time_utc)
    for category in open_categories:
        opening_date = category.opening_date
        

        if opening_date < time_utc:
            category.status_open = True
            category.save()

    closing_categories = Category.objects.filter(closing_date__lte=time_utc, status_open=True)
    for category in closing_categories:
        closing_date = category.closing_date
        if time_utc > closing_date:
            category.status_open = False
            category.save()

    return True


