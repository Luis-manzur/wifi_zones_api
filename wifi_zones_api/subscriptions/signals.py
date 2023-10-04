"""Subscription signals"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from wifi_zones_api.operations.models import Payment, Operation

# Models
from wifi_zones_api.subscriptions.models import Subscription


@receiver(post_save, sender=Subscription)
def charge_subscription(sender, instance: Subscription, created, **kwargs):
    if created:
        payment_description = f"{instance.start_date}  {instance.plan} plan subscription"
        amount = instance.plan.monthly_price if instance.billing_period == "monthly" else instance.plan.yearly_price
        payment = Payment()
        payment.amount = amount
        payment.description = payment_description
        operation = Operation()
        operation.user = instance.user
        operation.operation_type = "P"
        operation.prev_balance = instance.user.balance
        operation.post_balance = instance.user.balance - amount
        operation.save()
        payment.operation = operation
        payment.save()
