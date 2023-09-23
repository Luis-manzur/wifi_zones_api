from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LocationsConfig(AppConfig):
    name = "wifi_zones_api.locations"
    verbose_name = _("Locations")

    def ready(self):
        try:
            import wifi_zones_api.locations.signals  # noqa: F401
        except ImportError:
            pass
