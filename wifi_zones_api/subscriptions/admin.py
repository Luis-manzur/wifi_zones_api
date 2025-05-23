"""Subscription admin panel"""
# Django
from django.contrib import admin
import csv
from django.http import HttpResponse

# models
from wifi_zones_api.subscriptions.models import Plan, Subscription


class PlanAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "monthly_price")
    search_fields = ("name",)
    list_filter = ("monthly_price",)


admin.site.register(Plan, PlanAdmin)

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="subscription.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in modeladmin.model._meta.fields])

    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in modeladmin.model._meta.fields])

    return response

class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",  "plan", "billing_period", "auto_renew")
    list_filter = ("plan", "auto_renew", "billing_period", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Subscription, SubscriptionAdmin)
