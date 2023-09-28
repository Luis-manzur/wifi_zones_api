"""Locations URLs."""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import locations as locations_views
from .views import states as states_views

router = DefaultRouter()
router.register(r"sites", locations_views.LocationViewSet, basename="locations")
router.register(r"states", states_views.StateViewSet, basename="states")

urlpatterns = [
    path("", include(router.urls)),
]
