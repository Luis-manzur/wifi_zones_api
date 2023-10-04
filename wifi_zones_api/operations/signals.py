"""Operations signals"""

from django.db.models.signals import post_save
from django.dispatch import receiver

# Models
from wifi_zones_api.operations.models import Recharge


@receiver(post_save, sender=Recharge)
def add_user_balance(sender, instance: Recharge, created, **kwargs):
    if created:
        operation = instance.operation
        user = operation.user
        user.balance += instance.amount
        user.save()
