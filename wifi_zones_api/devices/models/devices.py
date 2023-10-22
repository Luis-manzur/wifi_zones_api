"""Device model"""

from django.core.validators import RegexValidator

# Django
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from wifi_zones_api.utils.models import WZModel


class Device(WZModel):
    """Device model.
    A device holds a user's device data for UC auto connection.
    """

    name = models.CharField()
    model = models.CharField()
    brand = models.CharField()
    mac_regex = RegexValidator(
        regex=r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$",
        message=_("Enter a valid MAC address."),
    )
    mac = models.CharField(max_length=17, validators=[mac_regex])

    user = models.ForeignKey("users.User", related_name="device", on_delete=models.CASCADE)
