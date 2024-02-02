import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from wifi_zones_api.external_apis.ruijie import login
from wifi_zones_api.external_apis.exchange_rates.api_caller import get_exchange_rates
from config.settings.base import env

logger = logging.getLogger("console")

settings_file = env('DJANGO_SETTINGS_MODULE')
class ExternalAPISConfig(AppConfig):
    name = "wifi_zones_api.external_apis"
    verbose_name = _("External API'S")

    def ready(self):
        if settings_file != "config.settings.test":
            login()
            get_exchange_rates()

        logger.info("external apis app started")
