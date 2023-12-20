import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from wifi_zones_api.external_apis.ruijie import login
from django.conf import settings

logger = logging.getLogger("console")

settings_file = settings.env('DJANGO_SETTINGS_MODULE')
class ExternalAPISConfig(AppConfig):
    name = "wifi_zones_api.external_apis"
    verbose_name = _("External API'S")

    def ready(self):
        if settings_file != "config.settings.test":
            login()
        logger.info("external apis app started")
