"""PagoMovil Viewset"""
# DRF
from drf_spectacular.utils import inline_serializer, extend_schema
from rest_framework import viewsets, mixins, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Models
from wifi_zones_api.operations.models import PagoMovil

# Serializer
from wifi_zones_api.operations.serializers.recharges import PagoMovilCreateModelSerializer

confirmation_inline_serializer = inline_serializer(
    name="PagoMovilConfirmationInlineSerializer",
    fields={"code": serializers.IntegerField(default=200), "Refpk": serializers.CharField()},
)

# Permissions
from wifi_zones_api.operations.permissions import HasPagoMovilPermission


class PagoMovilViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    serializer_class = PagoMovilCreateModelSerializer
    queryset = PagoMovil.objects.all()

    def get_permissions(self):
        """Assign permissions based on action."""
        permissions = [HasPagoMovilPermission, IsAuthenticated]
        return [p() for p in permissions]

    @extend_schema(
        responses={200: confirmation_inline_serializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        return Response({"code": 200, "Refpk": data["Refpk"]}, status=200)
