"""Plans views"""
# Django filters
from django_filters.rest_framework import DjangoFilterBackend

# DRF
from rest_framework import viewsets, mixins
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.subscriptions.models import Plan

# Serializer
from wifi_zones_api.subscriptions.serializers.plans import PlanModelSerializer, PlanListModelSerializer


class PlanViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.ListModelMixin):
    """Plan view set.
    Handle list and retrieve.
    """

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Plan.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return PlanListModelSerializer
        elif self.action == "retrieve":
            return PlanModelSerializer

    filter_backends = (OrderingFilter, SearchFilter, DjangoFilterBackend)
    search_fields = ("name",)
    ordering_fields = ("-created", "created")
    ordering = ("-created",)
