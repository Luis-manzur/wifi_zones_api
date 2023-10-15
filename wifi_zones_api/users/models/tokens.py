from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.authtoken.models import Token


class CustomToken(Token):
    """
    custom authorization token model.
    """
    device = models.OneToOneField(
        "devices.Device",
        related_name="auth_token",
        on_delete=models.CASCADE, verbose_name=_("Device")
    )
