"""States Views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.locations.models.states import State

# Serializer
from wifi_zones_api.locations.serializers.states import StateChoiceModelSerializer


class StateViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """State view set.
    Handle Venues list and retrieve.
    """

    queryset = State.objects.all()
    serializer_class = StateChoiceModelSerializer
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    ordering = ("name",)
