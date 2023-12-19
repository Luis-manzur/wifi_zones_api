"""Voucher URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import vouchers as vouchers_views

router = DefaultRouter()
router.register(r"", vouchers_views.VoucherViewSet, basename="vouchers")
urlpatterns = [
    path("", include(router.urls)),
]
