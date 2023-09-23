"""Locations admin panel"""
# Django
from django.contrib import admin

# models
from wifi_zones_api.locations.models import Location
from wifi_zones_api.utils.admin import admin_site


class VenueAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "state", "municipality")
    search_fields = ("name",)
    list_filter = ("state__name",)


admin_site.register(Location, VenueAdmin)
