from .base import *

DEBUG = False

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": "5432",
    }
}

#AWS Configurations

AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')

AWS_DEFAULT_ACL = None
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

AWS_STATIC_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/${AWS_STATIC_LOCATION}/'
STATICFILES_STORAGE = 'backend.storage_backends.StaticStorage'

AWS_PUBLIC_MEDIA_LOCATION = 'media/public'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/${AWS_PUBLIC_MEDIA_LOCATION}/'
DEFAU_FILE_STORAGE = 'backend.storage_backends.MediaStorage'

AWS_MEDIA_BUCKET_NAME= config('AWS_MEDIA_BUCKET_NAME')
AWS_PRIVATE_MEDIA_LOCATION = 'media/private'
MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/${AWS_PRIVATE_MEDIA_LOCATION}/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Celery Configuration Options
CELERY_TIMEZONE = "Africa/Nairobi"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 60 * 60
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_BROKER_BACKEND = config('CELERY_BROKER_BACKEND')