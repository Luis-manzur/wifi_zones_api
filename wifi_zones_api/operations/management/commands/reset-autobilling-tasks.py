"""Reset Auto billing tasks after restart"""

from datetime import timedelta

from dateutil.relativedelta import relativedelta
# Django
from django.core.management.base import BaseCommand
from wifi_zones_api.subscriptions.models import Subscription

# Task
from wifi_zones_api.subscriptions.tasks import remind_near_billing_date, bill_subscription


class Command(BaseCommand):
    help = "Recreates Auto billing tasks"

    def handle(self, *args, **options):
        subscriptions = Subscription.objects.filter(status="active", auto_renew=True)
        for subscription in subscriptions:
            if subscription.billing_period == "monthly":
                eta = subscription.created + relativedelta(months=1)
            elif subscription.billing_period == "yearly":
                eta = subscription.created + relativedelta(years=1)
            else:
                eta = subscription.created + relativedelta(days=1)
                bill_subscription.apply_async(args=(subscription.user.id, subscription.id), eta=eta)
                break
            remind_near_billing_date.apply_async(args=(subscription.user.id, subscription.id), eta=eta - timedelta(days=3))

            bill_subscription.apply_async(args=(subscription.user.id, subscription.id), eta=eta)
        self.stdout.write("Tasks generated successfully.")
