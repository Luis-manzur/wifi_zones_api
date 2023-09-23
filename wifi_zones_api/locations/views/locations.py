"""Locations Views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter

# Models
from wifi_zones_api.locations.models import Location

# Serializer
from wifi_zones_api.locations.serializers.locations import LocationModelSerializer, LocationListModelSerializer


class LocationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """Location view set.
    Handle list and retrieve.
    """

    queryset = Location.objects.all()

    def get_serializer_class(self):
        if self.action == "get":
            return LocationModelSerializer
        if self.action == "list":
            return LocationListModelSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    ordering_fields = ("-created", "created")
    ordering = ("-created",)
