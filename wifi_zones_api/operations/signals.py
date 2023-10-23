"""Operations signals"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from wifi_zones_api.devices.models import Device
# Models
from wifi_zones_api.operations.models import Payment, Recharge
# Notifications
from wifi_zones_api.utils.notifications import send_notification


@receiver(post_save, sender=Recharge)
def add_user_balance(sender, instance: Recharge, created, **kwargs):
    if created:
        operation = instance.operation
        user = operation.user
        user.balance += instance.amount
        user.save()

        devices = Device.objects.filter(user=user).values_list('token', flat=True)
        tokens = []
        for device in devices:
            tokens.append(device)
        response = send_notification("Recarga", f"Recarga exitosa por {instance.amount}", tokens)
        print(response)


@receiver(post_save, sender=Payment)
def take_user_balance(sender, instance: Payment, created, **kwargs):
    if created:
        operation = instance.operation
        user = operation.user
        user.balance -= instance.amount
        user.save()
