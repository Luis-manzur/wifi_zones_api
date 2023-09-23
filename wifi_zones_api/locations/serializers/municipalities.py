"""Municipalities serializers"""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.locations.models import Municipality


class MunicipalityBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ["name"]


class MunicipalityChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipality
        fields = ["name", "pk"]
