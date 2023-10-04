"""Operations URLs"""

# Django
from django.urls import include, path
# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import pago_movil as pago_movil_views

router = DefaultRouter()
router.register(r"recharge/pago-movil", pago_movil_views.PagoMovilViewSet, basename="pago-movil")

urlpatterns = [
    path("", include(router.urls)),
]
