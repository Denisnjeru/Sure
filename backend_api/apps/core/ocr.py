import os
import boto3
import io
import re
import datefinder
import pytesseract
import numpy as np
import cv2
import time

from decouple import config
from PIL import Image
from pdf2image import convert_from_path

def pytesseract_text_detection(document):
    filename = document

    # check file type
    parts = filename.split('.')
    extension = parts[-1]

    if extension == 'pdf':
        # Store Pdf with convert_from_path function
        images = convert_from_path(filename)
        images[0].save('images/tcc-image.jpg', 'JPEG')
        filename = 'images/tcc-image.jpg'

    img = np.array(Image.open(filename))

    norm_img = np.zeros((img.shape[0], img.shape[1]))
    img = cv2.normalize(img, norm_img, 0, 255, cv2.NORM_MINMAX)
    img = cv2.threshold(img, 100, 255, cv2.THRESH_BINARY)[1]
    img = cv2.GaussianBlur(img, (1, 1), 0)

    doc_text = pytesseract.image_to_string(img)

    return doc_text

def aws_text_detection(document):

    bucket = config('AWS_STORAGE_BUCKET_NAME')
    region = config('AWS_REGION')

    #Get the document from S3
    s3_connection = boto3.resource('s3')

    s3_object = s3_connection.Object(bucket,document)
    s3_response = s3_object.get()

    # Detect text in the document
    client = boto3.client('textract', region_name=region)

    #process using S3 object
    response = client.detect_document_text(
        Document={'S3Object': {'Bucket': bucket, 'Name': document}})

    #Get the text blocks
    blocks=response['Blocks']

    doc_text = ""
    for block in blocks:
        if block['BlockType'] == "LINE":
            doc_text += block['Text']

    return doc_text

def verify_tcc(document):
    """
    input: document path and name e.g /media/tcc/tcc.pdf
    output: returns an object containing the KRA PIN and expiry date of the document
            If the information cannot be extracted the values will be null
    """

    # initialize vaaribale to store text extracted from document
    text = ""
    expiry_date = None
    kra_pin = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        kra_pin = re.search(r'Identification Number ([\S\s]*?)has', text).group(1)
        kra_pin = kra_pin.strip()
    except Exception as e:
        pass

    try:
        # a generator will be returned by the datefinder module. I'm typecasting it to a list. Please read the note of caution provided at the bottom.
        expiry = re.search(r'up to(.*).', text, re.DOTALL).group(1).strip()
        matches = list(datefinder.find_dates(expiry))

        if len(matches) > 0:
            # date returned will be a datetime.datetime object. here we are only using the first match.
            expiry_date = matches[0]
    except Exception as e:
        pass

    return {
        "expiry_date": expiry_date,
        "kra_pin": kra_pin
    }

def verify_cr12(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    company_name = None
    cr12_ref = None
    shareholders = []

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        ref = re.search(r'REF NO: (.*)', text, re.DOTALL).group(1).strip()
        cr12_ref = ref
    except Exception as e:
        pass

    try:
        shareholders_info = re.search(r'Name of Directors and Shareholders of the above company with their particular are as follows(.*)Yours', text, re.DOTALL).group(1).strip()
        # for count, shareholder in enumerate(shareholders_info.splitlines()):
        #     if count != 0:
        #         shareholders.append(shareholder.split('|')[0])
    except Exception as e:
        pass

    try:
        company_name = re.search(r'COMPANY(.*)COMPANY NUMBER', text, re.M).group(1).strip()
    except Exception as e:
        pass

    return {
        "company_name": company_name,
        "cr12_ref_no": cr12_ref,
        "shareholders": shareholders
    }

def verify_nca(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    expiry_date = None
    serial_no = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        matches = re.search(r'Valid Until(.*)\n', text, re.M).group(1).strip()
        expiry = list(datefinder.find_dates(matches))
        if len(expiry) > 0:
            expiry_date = expiry[0]
    except Exception as e:
        pass

    try:
        serial_no = re.search(r'SERIAL No. (.*)\n', text, re.M).group(1).strip()
    except Exception as e:
        pass

    return {
        "serial_no": serial_no,
        "expiry_date": expiry_date,
    }

def verify_nationalid(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    names = None
    id_no = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        id_no_details = re.search(r'ID(.*)NAMES', text, re.M).group(1).strip()
        id_no = re.search(r'R(.*)F', id_no_details, re.M).group(1).strip().replace(":","").replace(" ","")
    except Exception as e:
        pass

    try:
        names = re.search(r'NAMES(.*)DATE OF B', text, re.M).group(1).strip()
    except Exception as e:
        pass

    return {
        "names": names,
        "id_no": id_no,
    }

def verify_businesspermit(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    business_name = None
    business_id = None
    year = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    if text.find("NAIROBI") != -1:
        try:
            business_name = re.search(r'ID(.*)Pin', text, re.M).group(1).strip()
            for letter in business_name:
                try:
                    int(letter)
                    business_name = business_name.replace(letter, "")
                except Exception as e:
                    pass
        except Exception as e:
            pass

        try:
            business_id_info = re.search(r'ID(.*)Pin', text, re.M).group(1).strip()[::-1]
            for letter in business_id_info:
                try:
                    int(letter)
                    if business_id == None:
                        business_id = ""
                    business_id += str(letter)
                except Exception as e:
                    break
        except Exception as e:
            pass

        try:
            year = re.search(r'YEAR(.*)Nairobi City County grants', text, re.M).group(1).strip()
        except Exception as e:
            pass

    return {
        "business_name": business_name,
        "business_id": business_id,
        "year": year
    }

def verify_poisonsboardcert(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    expiry_date = None
    company_name = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        matches = re.search(r'License expires on(.*)Trade Name', text, re.M).group(1).strip()
        expiry = list(datefinder.find_dates(matches))
        if len(expiry) > 0:
            expiry_date = expiry[0]
    except Exception as e:
        pass

    try:
        company_name = re.search(r'MAH Name(.*)Manufacturing Site', text, re.M).group(1).strip()
    except Exception as e:
        pass

    return {
        "expiry_date": expiry_date,
        "company_name": company_name
    }

def verify_pincert(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    pin = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    try:
        pin = re.search(r'Personal Identification Number(.*)This is to certify ', text, re.M).group(1).strip()
    except Exception as e:
        pass

    return {
        "pin": pin
    }

def verify_incorporationcert(document):
    # initialize vaaribale to store text extracted from document
    text = ""
    name = None
    date = None
    number = None

    if config('AWS_STORAGE_BUCKET_NAME') != '':
        if config('DEBUG') == True:
            # In a production environment strictly use aws textract
            text = aws_text_detection(document)
        else:
            # In a live developement environment strictly use aws textract
            text = aws_text_detection(document)
    else:
        # In a local developement environment strictly use google pytesseract
        text = pytesseract_text_detection(document)

    print(text)
    try:
        number = re.search(r'No. (.*)CERTIFICATE OF', text, re.M).group(1).strip()
    except Exception as e:
        pass

    try:
        name = re.search(r'CERTIFY that,(.*)is on', text, re.M).group(1).strip()
    except Exception as e:
        pass

    try:
        matches = re.search(r'is on this date (.*) Incorporated', text, re.M).group(1).strip()
        dates = list(datefinder.find_dates(matches))
        if len(dates) > 0:
            date = dates[0]
    except Exception as e:
        pass

    return {
        "name": name,
        "date": date,
        "number": number
    }


def sample_tcc():
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(config('AWS_STORAGE_BUCKET_NAME'))
    # for object_summary in bucket.objects.filter(Prefix="pdf/tcc/"):
    #     print(object_summary.key)
    #     print(verify_tcc(object_summary.key))
    for object_summary in bucket.objects.filter(Prefix="images/cr12/"):
        if (len(object_summary.key.split('.')) > 1):
            print(object_summary.key)
            print(verify_cr12(object_summary.key))
