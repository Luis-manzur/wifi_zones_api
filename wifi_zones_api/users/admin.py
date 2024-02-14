from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User  # Assuming your custom user model is in models.py
from django.utils.translation import gettext_lazy as _



class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("username", "password", "id_number", "phone_number")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "is_verified",
                    "is_client",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "id_number", "phone_number", "password1", "password2"),
            },
        ),
    )

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Modify the queryset as per your requirements
        queryset = queryset.exclude(username='Bancamiga')
        return queryset

admin.site.register(User, CustomUserAdmin)
