"""Transfers view sets"""

# Django filters
# DRF
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Models
from wifi_zones_api.operations.models import Transfer
# Serializer
from wifi_zones_api.operations.serializers.transfers import TransferCreateModelSerializer


# Utilities


class TransferViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Transfer view set"""

    serializer_class = TransferCreateModelSerializer

    def get_queryset(self):
        return Transfer.objects.all()

    def get_permissions(self):
        permissions = [IsAuthenticated]

        return [p() for p in permissions]
