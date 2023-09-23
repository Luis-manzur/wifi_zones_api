from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DevicesConfig(AppConfig):
    name = "wifi_zones_api.devices"
    verbose_name = _("Users")

    def ready(self):
        try:
            import wifi_zones_api.devices.signals  # noqa: F401
        except ImportError:
            pass
