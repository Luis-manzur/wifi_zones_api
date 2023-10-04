"""PagoMovil Viewset"""

# DRF
from rest_framework import viewsets, mixins

# Models
from wifi_zones_api.operations.models import PagoMovil
# Serializer
from wifi_zones_api.operations.serializers.recharges import PagoMovilCreateModelSerializer


class PagoMovilViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PagoMovilCreateModelSerializer
    queryset = PagoMovil.objects.all()
