from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Assuming your custom user model is in models.py
from wifi_zones_api.utils.admin import admin_site
admin_site.register(User, UserAdmin)
