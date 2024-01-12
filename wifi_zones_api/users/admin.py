from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Assuming your custom user model is in models.py

admin.site.register(User, UserAdmin)
