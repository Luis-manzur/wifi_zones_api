"""Subscription signals"""

from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from wifi_zones_api.operations.models import Payment, Operation
# Models
from wifi_zones_api.subscriptions.models import Subscription, Plan


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


def clear_cache(key):
    keys = cache.keys(f"*{key}*")
    for key in keys:
        cache.delete(key)


@receiver(post_save, sender=Plan)
def plan_update(sender, instance: Plan, created, **kwargs):
    clear_cache("plans")


@receiver(post_delete, sender=Plan)
def plan_delete(sender, instance: Plan, **kwargs):
    clear_cache("plans")
