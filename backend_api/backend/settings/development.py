from .base import *

DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "api.tendersure.co.ke", "*"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]


# DEBUG TOOLBAR SETTINGS

DEBUG_TOOLBAR_PANELS = [
    "debug_toolbar.panels.versions.VersionsPanel",
    "debug_toolbar.panels.timer.TimerPanel",
    "debug_toolbar.panels.settings.SettingsPanel",
    "debug_toolbar.panels.headers.HeadersPanel",
    "debug_toolbar.panels.request.RequestPanel",
    "debug_toolbar.panels.sql.SQLPanel",
    "debug_toolbar.panels.staticfiles.StaticFilesPanel",
    "debug_toolbar.panels.templates.TemplatesPanel",
    "debug_toolbar.panels.cache.CachePanel",
    "debug_toolbar.panels.signals.SignalsPanel",
    "debug_toolbar.panels.logging.LoggingPanel",
    "debug_toolbar.panels.redirects.RedirectsPanel",
    "debug_toolbar.panels.profiling.ProfilingPanel",
]


def show_toolbar(request):
    return True


DEBUG_TOOLBAR_CONFIG = {
    "INTERCEPT_REDIRECTS": False,
    "SHOW_TOOLBAR_CALLBACK": show_toolbar,
}


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

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

# AWS Configurations

AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_REGION = config("AWS_REGION")

# AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")

# AWS_DEFAULT_ACL = None
# AWS_S3_CUSTOM_DOMAIN = f"{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com"
# AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}

# AWS_STATIC_LOCATION = "static"
# STATICFILES_STORAGE = "backend.storage_backends.StaticStorage"

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")


MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# AWS_PUBLIC_MEDIA_LOCATION = "media/public"
# DEFAULT_FILE_STORAGE = "backend.storage_backends.MediaStorage"

AWS_MEDIA_BUCKET_NAME = config("AWS_MEDIA_BUCKET_NAME")
# AWS_PRIVATE_MEDIA_LOCATION = "media/private"
# MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/${AWS_PRIVATE_MEDIA_LOCATION}/"

# STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# MPESA Config
SHORTCODE = os.getenv("SHORTCODE")
CONSUMER_KEY = os.getenv("CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
SITE_URL = os.getenv("SITE_URL")

CELERY_TIMEZONE = "Africa/Nairobi"
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = "redis://localhost:6379"
CELERY_BROKER_BACKEND = "redis://localhost:6379"
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


#Register all CronJobs
CRONJOBS = [
    ("* * * * *", "apps.rfq.cron.open_close_rfq"),
    ("* * * * *", "apps.prequal.cron.open_close_prequal"),
    ("* * * * *", "apps.tender.cron.open_close_tender"),
    ('* * * * *', 'apps.auction.cron.open_close_auction')
]
