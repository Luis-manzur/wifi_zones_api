"""Voucher model"""
# Utils
from datetime import date

# Django
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Voucher(WZModel):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="vouchers", unique_for_date="date")
    location = models.ForeignKey("locations.Location", on_delete=models.CASCADE, related_name="vouchers")
    connection_code = models.CharField(max_length=16, unique_for_date="date")
    date = models.DateField(auto_now_add=True)
