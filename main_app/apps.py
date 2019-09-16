from django.apps import AppConfig
from django.db.models.signals import post_save


class MainAppConfig(AppConfig):
    name = 'main_app'

    def ready(self):
        import main_app.signals
