"""Subscription admin panel"""
# Django
from django.contrib import admin

# models
from wifi_zones_api.subscriptions.models import Plan


class PlanAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "monthly_price")
    search_fields = ("name",)
    list_filter = ("monthly_price",)


admin.site.register(Plan, PlanAdmin)
