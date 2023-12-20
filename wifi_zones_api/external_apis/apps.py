import logging

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

from wifi_zones_api.external_apis.ruijie import login

logger = logging.getLogger("console")


class ExternalAPISConfig(AppConfig):
    name = "wifi_zones_api.external_apis"
    verbose_name = _("External API'S")

    def ready(self):
        login()
        logger.info("external apis app started")
