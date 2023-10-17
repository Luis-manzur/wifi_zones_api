"""Subscriptions Serializers."""
# Django
from django.utils.translation import gettext_lazy as _
# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.subscriptions.models import Subscription, Plan
# Serializers
from wifi_zones_api.subscriptions.serializers.plans import PlanModelSerializer


class SubscriptionCreateModelSerializer(serializers.ModelSerializer):
    """Subscription create model serializer."""

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Subscription
        fields = ["user", "plan", "billing_period"]

    def validate(self, data):
        existing_subscription = Subscription.objects.filter(user=data["user"], status="active").exists()

        if existing_subscription:
            raise serializers.ValidationError(
                _("User already has an active subscription within the specified date range.")
            )

        plan: Plan = data["plan"]
        user = data["user"]

        if data["billing_period"] == "monthly":
            if plan.monthly_price > user.balance:
                raise serializers.ValidationError(_("Insufficient funds"))

        return data


class SubscriptionModelSerializer(serializers.ModelSerializer):
    """Subscription model serializer."""

    plan = PlanModelSerializer(read_only=True)

    class Meta:
        model = Subscription
        exclude = ["created", "modified", "user"]
