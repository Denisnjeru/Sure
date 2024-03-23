from django.apps import AppConfig


class PrequalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.prequal'

    def ready(self):
        import apps.prequal.signals
