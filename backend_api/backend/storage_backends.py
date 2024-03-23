from django.conf import settings
from decouple import config
from storages.backends.s3boto3 import S3Boto3Storage


class StaticStorage(S3Boto3Storage):
    location = "static"
    default_acl = "private"


class PrivateMediaStorage(S3Boto3Storage):
    bucket_name = config("AWS_MEDIA_BUCKET_NAME")
    location = config("AWS_PRIVATE_MEDIA_LOCATION")
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
