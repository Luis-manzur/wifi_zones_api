"""Devices Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.devices.models import Device


class DeviceListModelSerializer(serializers.ModelSerializer):
    """Devices list model serializer."""

    class Meta:
        model = Device
        exclude = ["token", "created", "modified", "user"]


class DeviceModelSerializer(serializers.ModelSerializer):
    """Devices model serializer."""

    class Meta:
        model = Device
        exclude = ["user"]


class DeviceLoginModelSerializer(DeviceModelSerializer):
    """Device Login serializer"""

    def get_fields(self):
        """
        Override to omit unique validation for `token` and 'device_id'.
        """
        fields = super().get_fields()

        if "device_id" in fields:
            fields["device_id"].validators = []

        if "token" in fields:
            fields["token"].validators = []

        return fields
