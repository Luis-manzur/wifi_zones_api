"""Operations admin panel"""
# Django
from django.contrib import admin
import csv
from django.http import HttpResponse

# models
from wifi_zones_api.operations.models import Operation

def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="operations.csv"'

    writer = csv.writer(response)
    writer.writerow([field.name for field in modeladmin.model._meta.fields])

    for obj in queryset:
        writer.writerow([getattr(obj, field.name) for field in modeladmin.model._meta.fields])

    return response

class OperationAdmin(admin.ModelAdmin):
    list_display = ("pk", "user",  "operation_type", "code")
    list_filter = ("user", "operation_type", "created")
    actions = [export_to_csv]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False

admin.site.register(Operation, OperationAdmin)
