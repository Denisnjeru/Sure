import datetime

from django import apps


def open_close_prequal():
    time_utc = datetime.datetime.now(datetime.timezone.utc)

    open_categories = apps.apps.get_model('prequal', 'Category').objects.filter(closing_date__gte=time_utc)
    for category in open_categories:
        opening_date = category.opening_date

        if opening_date < time_utc:
            category.is_open = True
            category.save()

    closing_categories = apps.apps.get_model('prequal', 'Category').objects.filter(closing_date__lte=time_utc, is_open=True)
    for category in closing_categories:
        closing_date = category.closing_date
        if time_utc > closing_date:
            category.is_open = False
            category.save()
    return True