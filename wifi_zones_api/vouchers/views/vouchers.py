"""Vouchers views"""

from drf_spectacular.utils import extend_schema

# DRF
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

# Models
from wifi_zones_api.vouchers.models import Voucher

# Serializers
from wifi_zones_api.vouchers.serializers import VoucherCreateModelSerializer, VoucherResponseSerializer


class VoucherViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    """Voucher view set.
    Handle create.
    """

    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    queryset = Voucher.objects.all()

    def get_serializer_class(self):
        if self.action == "create":
            return VoucherCreateModelSerializer

    @extend_schema(
        responses={201: VoucherResponseSerializer},
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        voucher_data = serializer.save()
        data = VoucherResponseSerializer(voucher_data).data
        return Response(data, status=status.HTTP_201_CREATED)
