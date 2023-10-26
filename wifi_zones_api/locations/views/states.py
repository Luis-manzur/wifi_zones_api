"""States Views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend
# DRF
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.locations.models.states import State
# Serializer
from wifi_zones_api.locations.serializers.states import StateChoiceModelSerializer
# Utils
from wifi_zones_api.utils import mixins as custom_mixins


class StateViewSet(viewsets.GenericViewSet, custom_mixins.CacheListModelMixin):
    """State view set.
    Handle Venues list and retrieve.
    """

    queryset = State.objects.all()
    serializer_class = StateChoiceModelSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering = ("name",)

    def get_cache_timeout(self):
        return 60 * 60 * 24
