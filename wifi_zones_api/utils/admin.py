"""Project custom admin site"""

# Django
from django.contrib import admin
from django.contrib.admin import site


class WZAdminSite(admin.AdminSite):
    def __init__(self, *args, **kwargs):
        super(WZAdminSite, self).__init__(*args, **kwargs)
        self._registry.update(site._registry)  # PART 2


admin_site = WZAdminSite(name="wzadmin")
