"""Operations admin panel"""
# Django
from django.contrib import admin
import csv
from django.http import HttpResponse

# models
from wifi_zones_api.operations.models import Operation, Recharge, PagoMovil, Payment

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="operations.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in modeladmin.model._meta.fields])

    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in modeladmin.model._meta.fields])

    return response

class OperationAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",  "operation_type", "code", "created")
    list_filter = ("user", "operation_type", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Operation, OperationAdmin)

class RechargeAdmin(admin.ModelAdmin):
    list_display = ("pk", "amount",  "payment_method", "created")
    list_filter = ("payment_method", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Recharge, RechargeAdmin)


class PMAdmin(admin.ModelAdmin):
    list_display = ("pk", "reference_number",  "origin_phone_number", "status", "bank")
    list_filter = ("status", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(PagoMovil, PMAdmin)


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("pk", "amount", "payment_method", "created")
    list_filter = ("payment_method", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Payment, PaymentAdmin)
