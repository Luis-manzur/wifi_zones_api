"""Operations URLs"""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import operations as operations_views
from .views import pago_movil as pago_movil_views
from .views import transfers as transfers_views

router = DefaultRouter()
router.register(r"recharge/pago-movil", pago_movil_views.PagoMovilViewSet, basename="pago-movil")
router.register(r"", operations_views.OperationsViewSet, basename="operations")
router.register(r"transfer/internal", transfers_views.TransferViewSet, basename="transfers")

urlpatterns = [
    path("", include(router.urls)),
]
