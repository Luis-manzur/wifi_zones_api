"""Recharges serializers"""
import json
# Utils
from datetime import datetime

# Django
from django.core.exceptions import ObjectDoesNotExist
# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.operations.models import Recharge, PagoMovil, Operation
from wifi_zones_api.users.models import User
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

    def validate_PhoneOrig(self, data):
        try:
            user = User.objects.get(phone_number=data)
            self.context["user"] = user
        except ObjectDoesNotExist:
            raise serializers.ValidationError('No user associated with that phone number')
        return data

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
        pago_movil.request_body = json.dumps(self.initial_data)

        # Create the recharge instance
        recharge = Recharge()
        recharge.amount = amount
        recharge.payment_method = "PM"

        # Create the Operation Instance
        operation = Operation()
        operation.user = self.context["user"]
        operation.operation_type = "R"
        operation.prev_balance = operation.user.balance
        operation.post_balance = operation.user.balance + amount

        # Save the PagoMovil instance
        operation.save()
        recharge.operation = operation
        recharge.save()
        pago_movil.recharge = recharge
        pago_movil.save()

        return validated_data
