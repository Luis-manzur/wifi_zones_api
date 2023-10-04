"""Payments models"""

# Django
from django.core.validators import MinValueValidator
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Payment(WZModel):
    """Recharge Model."""

    operation = models.ForeignKey("operations.Operation", related_name="payment", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])

    PAYMENT_METHOD = [
        ("W", "Wallet"),
        ("C", "Coupon"),
    ]

    description = models.CharField(max_length=100)

    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD, default="W")
