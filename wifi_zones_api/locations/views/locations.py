"""Locations Views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.locations.models import Location

# Serializer
from wifi_zones_api.locations.serializers.locations import LocationModelSerializer, LocationListModelSerializer


class LocationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """Location view set.
    Handle list and retrieve.
    """

    queryset = Location.objects.all()
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return LocationModelSerializer
        if self.action == "list":
            return LocationListModelSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    ordering_fields = ("-created", "created")
    ordering = ("-created",)
