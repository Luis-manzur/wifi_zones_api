"""Devices Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.devices.models import Device


class DeviceListModelSerializer(serializers.ModelSerializer):
    """Devices list model serializer."""

    class Meta:
        model = Device
        exclude = ["mac", "model", "created", "modified", "user"]


class DeviceModelSerializer(serializers.ModelSerializer):
    """Devices model serializer."""

    class Meta:
        model = Device
        exclude = ["user"]
