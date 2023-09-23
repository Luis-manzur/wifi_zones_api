"""Location Serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.locations.models import Location

# Serializers
from wifi_zones_api.locations.serializers.municipalities import MunicipalityBasicSerializer
from wifi_zones_api.locations.serializers.states import StateBasicSerializer


class LocationListModelSerializer(serializers.ModelSerializer):
    """Location model serializer."""

    class Meta:
        model = Location
        exclude = ["created", "modified", "state", "municipality"]


class LocationModelSerializer(serializers.ModelSerializer):
    """Location model serializer."""

    state = StateBasicSerializer(read_only=True)
    municipality = MunicipalityBasicSerializer(read_only=True)

    class Meta:
        model = Location
        exclude = ["created", "modified"]
