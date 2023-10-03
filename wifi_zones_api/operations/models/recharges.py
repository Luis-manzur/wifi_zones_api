"""Recharge models"""

# Django
from django.core.validators import MinValueValidator
from django.db import models

# Utilities
from wifi_zones_api.utils.consts import BANKS
from wifi_zones_api.utils.models import WZModel


class Recharge(WZModel):
    """Recharge Model."""

    operation = models.ForeignKey("operations.Operation", related_name="recharge", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])

    PAYMENT_METHOD = [
        ("PM", "Pago móvil"),
        ("DC", "Debit card"),
    ]

    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD, default="PM")


class PagoMovil(WZModel):
    recharge = models.ForeignKey(
        "operations.Recharge", related_name="pago_movil", on_delete=models.DO_NOTHING,
    )
    operation_time_stamp = models.DateTimeField()
    reference_number = models.CharField(max_length=10, unique=True)
    origin_phone_number = models.CharField()
    recipient_phone_number = models.CharField()
    status = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    ref_pk = models.CharField(max_length=100, unique=True)

    bank = models.CharField(max_length=4, choices=BANKS, default="0172")

    request_body = models.JSONField()
