"""Transfers models"""

# Django
from django.core.validators import MinValueValidator
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Transfer(WZModel):
    """Transfers Model."""
    sender_operation = models.ForeignKey("operations.Operation", related_name="sent_transfers",
                                         on_delete=models.CASCADE)
    receiver_operation = models.ForeignKey("operations.Operation", related_name="received_transfers",
                                           on_delete=models.CASCADE)
    sender = models.ForeignKey("users.User", related_name="sent_transfers", on_delete=models.DO_NOTHING)
    receiver = models.ForeignKey("users.User", related_name="received_transfers", on_delete=models.DO_NOTHING)

    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])
