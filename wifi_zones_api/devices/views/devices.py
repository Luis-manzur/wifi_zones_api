"""Devices Views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend
# DRF
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated

# Models
from wifi_zones_api.devices.models import Device
# Serializer
from wifi_zones_api.devices.serializers.devices import DeviceModelSerializer, DeviceListModelSerializer
# Utilities
from wifi_zones_api.utils.permissions import IsObjectOwner


class DeviceViewSet(viewsets.ModelViewSet):
    """Device view set.
    Handle list and retrieve.
    """
    pagination_class = None

    queryset = Device.objects.all()

    def get_permissions(self):
        permissions = [IsAuthenticated, IsObjectOwner]
        if self.action == "create":
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    def get_serializer_class(self):
        if self.action == "list":
            return DeviceListModelSerializer
        else:
            return DeviceModelSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name", "model", "brand")
    ordering_fields = ("-created", "created")
    ordering = ("-created",)
