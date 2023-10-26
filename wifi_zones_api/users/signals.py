"""Users signals"""
from django.core.cache import cache
# django
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# Models
from wifi_zones_api.users.models import User


def clear_cache(key):
    keys = cache.keys(f"*{key}*")
    for key in keys:
        cache.delete(key)


@receiver(post_save, sender=User)
def location_update(sender, instance: User, created, **kwargs):
    clear_cache(instance.username)


@receiver(post_delete, sender=User)
def location_delete(sender, instance: User, **kwargs):
    clear_cache(instance.username)
