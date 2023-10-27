"""Operations signals"""

from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver

from wifi_zones_api.devices.models import Device
# Models
from wifi_zones_api.operations.models import Payment, Recharge, Operation, Transfer
# Notifications
from wifi_zones_api.utils.notifications import send_notification


def clear_cache(key):
    keys = cache.keys(f"*{key}*")
    for key in keys:
        cache.delete(key)


@receiver(post_save, sender=Recharge)
def add_user_balance(sender, instance: Recharge, created, **kwargs):
    if created:
        operation = instance.operation
        user = operation.user
        user.balance += instance.amount
        user.save()

        devices = Device.objects.filter(user=user).values_list("token", flat=True)
        tokens = []
        for device in devices:
            tokens.append(device)
        send_notification("Recarga", f"Recarga exitosa por {instance.amount}", tokens)


@receiver(post_save, sender=Payment)
def take_user_balance(sender, instance: Payment, created, **kwargs):
    if created:
        operation = instance.operation
        user = operation.user
        user.balance -= instance.amount
        user.save()


@receiver(post_save, sender=Transfer)
def make_transfer(sender, instance: Transfer, created, **kwargs):
    if created:
        sender = instance.sender
        sender.balance -= instance.amount
        sender.save()

        receiver = instance.receiver
        receiver.balance += instance.amount
        receiver.save()

        devices = Device.objects.filter(user=receiver).values_list("token", flat=True)
        tokens = []
        for device in devices:
            tokens.append(device)
        send_notification("Transferencia", f"Has recibido una transferencia de {sender} por {instance.amount}", tokens)


@receiver(post_save, sender=Operation)
def operation_update(sender, instance: Operation, created, **kwargs):
    clear_cache(f"operations/{instance.user.pk}")
