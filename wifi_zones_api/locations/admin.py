"""Locations admin panel"""
# Django

from django.contrib import admin

# models
from wifi_zones_api.locations.models import Location


class VenueAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "state", "municipality")
    search_fields = ("name",)
    list_filter = ("state__name",)


admin.site.register(Location, VenueAdmin)
