"""Group serializers"""

from django.contrib.auth.models import Group
from rest_framework import serializers


class GroupListSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    def get_permissions(self, obj: Group) -> int:
        return obj.permissions.count()

    class Meta:
        model = Group
        fields = ('id', 'name', 'permissions')


class GroupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
