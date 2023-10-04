"""Subscription admin panel"""
# Django
from django.contrib import admin

# models
from wifi_zones_api.subscriptions.models import Plan
from wifi_zones_api.utils.admin import admin_site


class PlanAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "monthly_price")
    search_fields = ("name",)
    list_filter = ("monthly_price",)


admin_site.register(Plan, PlanAdmin)
