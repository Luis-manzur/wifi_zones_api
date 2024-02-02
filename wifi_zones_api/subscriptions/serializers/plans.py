"""Plans Serializers."""
from decimal import Decimal
# Django REST Framework
from rest_framework import serializers

# Django
from django.core.cache import cache

# Models
from wifi_zones_api.subscriptions.models import Plan


class PlanListModelSerializer(serializers.ModelSerializer):
    """Plan list model serializer."""
    monthly_price = serializers.SerializerMethodField()
    yearly_price = serializers.SerializerMethodField()

    def get_monthly_price(self, obj):
        exchange_rate = cache.get('exchange_rate')
        return obj.monthly_price * Decimal(str(exchange_rate))

    def get_yearly_price(self, obj):
        exchange_rate = cache.get('exchange_rate')
        return obj.yearly_price * Decimal(str(exchange_rate))

    class Meta:
        model = Plan
        fields = ["name", "yearly_price", "monthly_price", "id"]


class PlanModelSerializer(serializers.ModelSerializer):
    """Plan model serializer."""

    monthly_price = serializers.SerializerMethodField()
    yearly_price = serializers.SerializerMethodField()
    daily_price = serializers.SerializerMethodField()

    def get_monthly_price(self, obj):
        exchange_rate = cache.get('exchange_rate')
        return obj.monthly_price * Decimal(str(exchange_rate))

    def get_yearly_price(self, obj):
        exchange_rate = cache.get('exchange_rate')
        return obj.yearly_price * Decimal(str(exchange_rate))

    def get_daily_price(self, obj):
        exchange_rate = cache.get('exchange_rate')
        return obj.daily_price * Decimal(str(exchange_rate))

    class Meta:
        model = Plan
        exclude = ["created", "modified"]
