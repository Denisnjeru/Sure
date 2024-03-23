import datetime

import pytz


def supplier_response_files(instance, filename):
    year = datetime.datetime.now().year
    return "%s/%s/%s/%s/%s/%s" % (
        instance.job.company.company_name.replace(" ", "_"),
        instance.job.job_code,
        instance.question.section.category.unique_reference,
        instance.supplier.company_name.replace(" ", "_"),
        year,
        filename,
    )

def clean_date_time(date_string):    
    # date_format = "%Y-%m-%d %I:%M %p"
    # date_object = datetime.datetime.strptime(date_string, date_format)
    utc = pytz.UTC
    date_object = date_string.replace(tzinfo=utc)
    return date_object