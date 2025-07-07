from django.apps import AppConfig


class AppidentityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'appidentity'

    def ready(self):
        import appidentity.signals