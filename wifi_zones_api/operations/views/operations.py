"""Operations view sets"""

# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.operations.models import Operation

# Serializer
from wifi_zones_api.operations.serializers.operations import OperationListModelSerializer

# Utilities
from wifi_zones_api.utils.permissions import IsObjectOwner


class OperationsViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """Operation view set"""

    lookup_field = "code"
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("code", "recharge__amount")
    filterset_fields = ["operation_type"]
    ordering_fields = ("-created", "created")
    ordering = ("-created",)

    def get_queryset(self):
        return Operation.objects.filter(user=self.request.user)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsObjectOwner]

        return [p() for p in permissions]

    serializer_class = OperationListModelSerializer
    queryset = Operation.objects.all()
