"""Subscriptions views"""
# Django
from django.utils.translation import gettext_lazy as _
# Django filters
from django_filters.rest_framework import DjangoFilterBackend
# DRF
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets, mixins, serializers, status
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

confirmation_inline_serializer = inline_serializer(
    name="VerifyInlineSerializer", fields={"message": serializers.CharField()}
)


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

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    @action(detail=True, methods=["delete"], url_path="cancel")
    def cancel_subscription(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = "canceled"
        subscription.save()
        return Response({"message": _("Subscription canceled.")})

    @extend_schema(
        responses={201: SubscriptionModelSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        subscription = serializer.save()
        data = SubscriptionModelSerializer(subscription).data
        return Response(data, status=status.HTTP_201_CREATED)
