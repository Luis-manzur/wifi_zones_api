"""subscriptions plans """
import datetime

# Utils
from dateutil.relativedelta import relativedelta

# Django
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

# Utilities
from wifi_zones_api.utils.models import WZModel


class Subscription(WZModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("canceled", "Canceled"),
        ("expired", "Expired"),
    ]

    BILLING_PERIOD_CHOICES = [
        ("monthly", "Monthly"),
        ("yearly", "Yearly"),
        ("daily", "Daily"),
    ]

    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="subscription")
    plan = models.ForeignKey("subscriptions.Plan", on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    billing_period = models.CharField(max_length=10, choices=BILLING_PERIOD_CHOICES)
    auto_renew = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")

    def save(self, *args, **kwargs):
        is_new_instance = self.pk is None  # Check if the primary key is None

        if is_new_instance:
            existing_subscription = Subscription.objects.filter(user=self.user, status="active").exists()
            if existing_subscription:
                raise ValidationError(_("User already has an active subscription within the specified date range."))

            if self.billing_period == "monthly":
                self.start_date = datetime.date.today()
                self.end_date = self.start_date + relativedelta(months=1)
            elif self.billing_period == "yearly":
                self.end_date = self.start_date + relativedelta(years=1)
            else:
                raise ValidationError(_("Invalid billing period."))
        super().save(*args, **kwargs)
