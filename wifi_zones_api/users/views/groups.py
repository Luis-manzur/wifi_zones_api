from django.contrib.auth.models import Group
from rest_framework import viewsets

from wifi_zones_api.users.serializers.groups import GroupListSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer
