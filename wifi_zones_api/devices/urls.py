"""Devices URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import devices as devices_views

router = DefaultRouter()
router.register(r"", devices_views.DeviceViewSet, basename="devices")

urlpatterns = [
    path("", include(router.urls)),
]
