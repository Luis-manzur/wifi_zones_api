"""Users admin panel"""
# Django
from django.contrib import admin

# models
from wifi_zones_api.users.models import User


class UserAdmin(admin.ModelAdmin):
    fields = ('groups',)
    list_display = ("pk", "email", "username", "first_name", "last_name")
    search_fields = ("username",)


admin.site.register(User, UserAdmin)
