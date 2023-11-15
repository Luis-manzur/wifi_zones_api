"""Subscription tasks"""

# Celery
from celery import shared_task

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Models
from wifi_zones_api.subscriptions.models import Subscription
from wifi_zones_api.users.models import User

# Notifications
from wifi_zones_api.utils.notifications import send_notification, get_user_devices_tokens


@shared_task()
def remind_near_billing_date(user_id, subscription_id):
    user = User.objects.get(pk=user_id)
    current_subscription: Subscription = Subscription.objects.get(pk=subscription_id)

    if current_subscription.status != "active" or not current_subscription.auto_renew:
        return

    tokens = get_user_devices_tokens(user)
    send_notification("Recordatorio", f"Le recordamos que su plan se auto renovara en 3 días.", tokens)


@shared_task()
def bill_subscription(user_id, subscription_id):
    user = User.objects.get(pk=user_id)
    current_subscription: Subscription = Subscription.objects.get(pk=subscription_id)

    if current_subscription.status != "active" or not current_subscription.auto_renew:
        return

    plan = current_subscription.plan

    insufficient_funds = False

    if current_subscription.billing_period == "monthly":
        if plan.monthly_price > user.balance:
            insufficient_funds = True

    if current_subscription.billing_period == "yearly":
        if plan.yearly_price > user.balance:
            insufficient_funds = True

    if current_subscription.billing_period == "daily":
        if plan.daily_price > user.balance:
            insufficient_funds = True

    if insufficient_funds:
        tokens = get_user_devices_tokens(user)
        send_notification("Subscripción cancelada", f"Fondos insuficientes.", tokens)
        return

    Subscription(user=user, plan=plan, billing_period=current_subscription.billing_period)
    tokens = get_user_devices_tokens(user)
    send_notification("Subscripción renovada", f"Tu plan {plan.name} ha sido renovado.", tokens)


@shared_task()
def send_receipt_email(user_id, subscription_id, amount):
    """Send receipt to user when subscription billed"""
    user = User.objects.get(pk=user_id)
    subscription: Subscription = Subscription.objects.get(pk=subscription_id)
    items = [{"name": f"Plan {subscription.plan.name} / {subscription.billing_period}", "amount": amount}]
    subject = "Recibo de Subscripción".format(user)
    from_email = settings.DEFAULT_FROM_EMAIL
    content = render_to_string(
        "emails/receipt.html",
        {"message": subject, "title": "Recibo de Subscripción", "items": items},
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
