from django.apps import AppConfig


class RfqConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.rfq'

    def ready(self):
        import apps.rfq.signals