"""Operations view sets"""

# DRF
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

# Models
from wifi_zones_api.operations.models import Operation

# Serializer
from wifi_zones_api.operations.serializers.operations import OperationListModelSerializer

# Utilities
from wifi_zones_api.utils.permissions import IsObjectOwner


class OperationsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsObjectOwner]

        return [p() for p in permissions]

    serializer_class = OperationListModelSerializer
    queryset = Operation.objects.all()
