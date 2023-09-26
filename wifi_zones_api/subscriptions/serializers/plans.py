"""Plans Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.subscriptions.models import Plan


class PlanListModelSerializer(serializers.ModelSerializer):
    """Plan list model serializer."""

    class Meta:
        model = Plan
        fields = ["name", "yearly_price", "monthly_price", "id"]


class PlanModelSerializer(serializers.ModelSerializer):
    """Plan model serializer."""

    class Meta:
        model = Plan
        exclude = ["created", "modified"]
