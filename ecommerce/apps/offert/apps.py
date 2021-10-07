from django.apps import AppConfig


class OffertConfig(AppConfig):
    name = 'ecommerce.apps.offert'

    def ready(self):
        import ecommerce.apps.offert.signals
