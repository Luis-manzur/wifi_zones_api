from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "wifi_zones_api.operations"
    verbose_name = _("Operations")

    def ready(self):
        try:
            import wifi_zones_api.operations.signals  # noqa: F401
        except ImportError:
            pass
