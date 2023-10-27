"""Transfers view sets"""
# Django
from django.utils.translation import gettext_lazy as _
# DRF
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from wifi_zones_api.operations.models import Transfer
# Serializer
from wifi_zones_api.operations.serializers.transfers import TransferCreateModelSerializer

confirmation_inline_serializer = inline_serializer(
    name="VerifyInlineSerializer", fields={"message": serializers.CharField()}
)


class TransferViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Transfer view set"""

    serializer_class = TransferCreateModelSerializer

    def get_queryset(self):
        return Transfer.objects.all()

    def get_permissions(self):
        permissions = [IsAuthenticated]

        return [p() for p in permissions]

    @extend_schema(
        responses={201: inline_serializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": _("Successful Transfer.")})
