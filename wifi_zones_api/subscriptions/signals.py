"""Subscription signals"""
# Utilities
from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta

# Django
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Models
from wifi_zones_api.operations.models import Payment, Operation
from wifi_zones_api.subscriptions.models import Subscription, Plan

# Task
from wifi_zones_api.subscriptions.tasks import remind_near_billing_date, bill_subscription, send_receipt_email


@receiver(post_save, sender=Subscription)
def charge_subscription(sender, instance: Subscription, created, **kwargs):
    if created:
        payment_description = f"{instance.start_date}  {instance.plan} plan subscription"
        amount = (
            instance.plan.monthly_price
            if instance.billing_period == "monthly"
            else instance.plan.yearly_price
            if instance.billing_period == "yearly"
            else instance.plan.daily_price
        )
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
        send_receipt_email.delay(instance.user.id, instance.id, amount)


@receiver(post_save, sender=Subscription)
def auto_renew_subscription(sender, instance: Subscription, created, **kwargs):
    if created:
        if instance.billing_period == "monthly":
            eta = datetime.now() + relativedelta(months=1)
        elif instance.billing_period == "yearly":
            eta = datetime.now() + relativedelta(years=1)
        else:
            return
        remind_near_billing_date.apply_async(args=(instance.user.id, instance.id), eta=eta - timedelta(days=3))

        bill_subscription.apply_async(args=(instance.user.id, instance.id), eta=eta)


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
