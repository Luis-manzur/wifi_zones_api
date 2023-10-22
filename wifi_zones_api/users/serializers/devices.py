"""FCM Device serializer"""
# Models
from fcm_django.models import FCMDevice
# DRF
from rest_framework import serializers


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = (
            "name",
            "registration_id",
            "device_id",
            "active",
            "type",
        )

    def create(self, data):
        registration_id = data.pop('registration_id')
        device = FCMDevice.objects.get_or_create(registration_id=registration_id, default=data)
        device.save()
        return device
