"""Operations signals"""
from django.core.cache import cache
# django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Models
from wifi_zones_api.locations.models import Location, State


def clear_cache(key):
    keys = cache.keys(f"*{key}*")
    for key in keys:
        cache.delete(key)


@receiver(post_save, sender=Location)
def location_update(sender, instance: Location, created, **kwargs):
    clear_cache("sites")


@receiver(post_delete, sender=Location)
def location_delete(sender, instance: Location, **kwargs):
    clear_cache("sites")


@receiver(post_save, sender=State)
def state_update(sender, instance: State, created, **kwargs):
    clear_cache("states")


@receiver(post_delete, sender=State)
def state_delete(sender, instance: State, **kwargs):
    clear_cache("states")
