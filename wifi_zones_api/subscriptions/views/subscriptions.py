"""Subscriptions views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from wifi_zones_api.subscriptions.models import Subscription

# Serializer
from wifi_zones_api.subscriptions.serializers.subscriptions import (
    SubscriptionModelSerializer,
    SubscriptionCreateModelSerializer,
)

# Utilities
from wifi_zones_api.utils.permissions import IsObjectOwner


class SubscriptionViewSet(
    viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin
):
    """Subscription view set.
    Handle list and retrieve.
    """

    def get_serializer_class(self):
        if self.action == "create":
            return SubscriptionCreateModelSerializer
        else:
            return SubscriptionModelSerializer

    def get_queryset(self):
        user = self.request.user
        return Subscription.objects.filter(user=user)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsObjectOwner]
        if self.action == "create":
            permissions = [IsAuthenticated]

        return [p() for p in permissions]

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    ordering_fields = ("-created", "created")
    ordering = ("-created",)

    @action(detail=True, methods=["post"])
    def cancel_subscription(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = "canceled"
        subscription.save()
        return Response({"message": "Subscription canceled."})
