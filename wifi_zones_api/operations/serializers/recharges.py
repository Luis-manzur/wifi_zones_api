"""Recharges serializers"""

# Utils
from datetime import datetime

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.operations.models import Recharge, PagoMovil
# Utilities
from wifi_zones_api.utils.consts import BANKS


class RechargeModelSerializer(serializers.ModelSerializer):
    """Recharge model serializer."""

    class Meta:
        model = Recharge
        exclude = ["modified", "created", "id"]


class PagoMovilModelSerializer(serializers.ModelSerializer):
    """Pago Movil model serializer."""

    class Meta:
        model = PagoMovil
        exclude = ["origin_phone_number", "recipient_phone_number", "status", "ref_pk"]


class PagoMovilCreateModelSerializer(serializers.Serializer):
    """Pago Movil create serializer."""

    BancoOrig = serializers.ChoiceField(choices=BANKS)
    FechaMovimiento = serializers.DateField()
    HoraMovimiento = serializers.TimeField()
    NroReferencia = serializers.CharField()
    PhoneOrig = serializers.CharField()
    PhoneDest = serializers.CharField()
    Status = serializers.CharField()
    Descripcion = serializers.CharField()
    Amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    Refpk = serializers.CharField()

    def create(self, validated_data):
        # Extract the data from the serializer
        banco_orig = validated_data["BancoOrig"]
        fecha_movimiento = validated_data["FechaMovimiento"]
        hora_movimiento = validated_data["HoraMovimiento"]
        nro_referencia = validated_data["NroReferencia"]
        phone_orig = validated_data["PhoneOrig"]
        phone_dest = validated_data["PhoneDest"]
        status = validated_data["Status"]
        descripcion = validated_data["Descripcion"]
        amount = validated_data["Amount"]
        ref_pk = validated_data["Refpk"]

        # Create a PagoMovil instance
        pago_movil = PagoMovil()
        pago_movil.operation_time_stamp = datetime.combine(fecha_movimiento, hora_movimiento)
        pago_movil.reference_number = nro_referencia
        pago_movil.origin_phone_number = phone_orig
        pago_movil.recipient_phone_number = phone_dest
        pago_movil.status = status
        pago_movil.description = descripcion
        pago_movil.ref_pk = ref_pk
        pago_movil.bank = banco_orig
        pago_movil.recharge.amount = amount
        pago_movil.recharge.payment_method = "PM"

        # Save the PagoMovil instance
        pago_movil.save()

        return validated_data
