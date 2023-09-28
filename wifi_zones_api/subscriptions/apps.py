from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SubscriptionsConfig(AppConfig):
    name = "wifi_zones_api.subscriptions"
    verbose_name = _("Subscription")

    def ready(self):
        try:
            import wifi_zones_api.subscriptions.signals  # noqa: F401
        except ImportError:
            pass
