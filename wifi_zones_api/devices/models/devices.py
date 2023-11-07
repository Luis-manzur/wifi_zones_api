"""Device model"""

# Django
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Device(WZModel):
    """Device model.
    A device holds a user's device data for UC auto connection.
    """

    OS = [("android", "android"), ("ios", "ios")]

    name = models.CharField()
    token = models.CharField(unique=True)
    os = models.CharField(choices=OS, default="android")
    user = models.ForeignKey("users.User", related_name="device", on_delete=models.CASCADE)
