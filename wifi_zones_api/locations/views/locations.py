"""Locations Views"""
# Django
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

# Utils
from wifi_zones_api.utils import mixins as custom_mixins


class LocationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, custom_mixins.CacheListModelMixin):
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

    def get_cache_timeout(self):
        return 60 * 60 * 12

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    ordering_fields = ("-created", "created")
    ordering = ("-created",)
