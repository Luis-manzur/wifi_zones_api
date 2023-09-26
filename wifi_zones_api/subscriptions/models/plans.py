"""Plans models"""
# Django
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Plan(WZModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    yearly_price = models.DecimalField(max_digits=8, decimal_places=2)
    monthly_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name
