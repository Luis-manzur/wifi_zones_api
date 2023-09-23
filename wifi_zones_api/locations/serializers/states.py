"""States serializers"""

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.locations.models import State

# Serializers
from wifi_zones_api.locations.serializers.municipalities import MunicipalityChoiceSerializer


class StateBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["name"]


class StateChoiceModelSerializer(serializers.ModelSerializer):
    municipalities = MunicipalityChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ["name", "pk", "municipalities"]
