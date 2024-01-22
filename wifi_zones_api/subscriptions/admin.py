"""Subscription admin panel"""
# Django
from django.contrib import admin

# models
from wifi_zones_api.subscriptions.models import Plan, Subscription


class PlanAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "monthly_price")
    search_fields = ("name",)
    list_filter = ("monthly_price",)


admin.site.register(Plan, PlanAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",  "plan", "billing_period", "auto_renew")
    list_filter = ("plan", "auto_renew", "billing_period")

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Subscription, SubscriptionAdmin)
