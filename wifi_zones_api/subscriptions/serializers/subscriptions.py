"""Subscriptions Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.subscriptions.models import Subscription

# Serializers
from wifi_zones_api.subscriptions.serializers.plans import PlanModelSerializer


class SubscriptionCreateModelSerializer(serializers.ModelSerializer):
    """Subscription create model serializer."""

    class Meta:
        model = Subscription
        fields = "__all__"


class SubscriptionModelSerializer(serializers.ModelSerializer):
    """Subscription model serializer."""

    plan = PlanModelSerializer(read_only=True)

    class Meta:
        model = Subscription
        exclude = ["created", "modified", "user"]
