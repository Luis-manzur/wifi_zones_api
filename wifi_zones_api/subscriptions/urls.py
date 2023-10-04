"""Subscriptions URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

from .views import plans as plans_views

# Views
from .views import subscriptions as subscriptions_views

router = DefaultRouter()
router.register(r"membership", subscriptions_views.SubscriptionViewSet, basename="subscription")
router.register(r"plans", plans_views.PlanViewSet, basename="plans")

urlpatterns = [
    path("", include(router.urls)),
]
