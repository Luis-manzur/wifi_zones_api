"""Operations models"""
# Utils
import uuid

# Django
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Operation(WZModel):
    """Operation model."""

    user = models.ForeignKey("users.User", related_name="operations", on_delete=models.CASCADE)

    prev_balance = models.DecimalField(max_digits=10, decimal_places=2)
    post_balance = models.DecimalField(max_digits=10, decimal_places=2)

    code = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    OPERATION_TYPES = [
        ("R", "Recharge"),
        ("P", "Payment"),
    ]

    operation_type = models.CharField(max_length=1, choices=OPERATION_TYPES, default="R")
