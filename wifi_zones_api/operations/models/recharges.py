"""Recharge models"""
# Utils

# Django
from django.core.validators import MinValueValidator
from django.db import models

# Utilities
from wifi_zones_api.utils.models import WZModel


class Recharge(WZModel):
    """Recharge Model."""

    operation = models.ForeignKey("operations.Operation", related_name="recharge", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.00)])

    PAYMENT_METHOD = [
        ("PM", "Pago móvil"),
        ("DC", "Debit card"),
    ]

    payment_method = models.CharField(max_length=2, choices=PAYMENT_METHOD, default="PM")


class PagoMovil(WZModel):
    recharge = models.ForeignKey(
        "operations.Recharge", related_name="pago_movil", on_delete=models.DO_NOTHING,
    )
    operation_time_stamp = models.DateTimeField()
    reference_number = models.CharField(max_length=10, unique=True)
    origin_phone_number = models.CharField()
    recipient_phone_number = models.CharField()
    status = models.CharField(max_length=10)
    description = models.CharField(max_length=255)
    ref_pk = models.CharField(max_length=100, unique=True)

    BANKS = [
        ("0102", "Banco de Venezuela, S.A.C.A."),
        ("0104", "Venezolano de Crédito"),
        ("0105", "Mercantil"),
        ("0108", "Provincial"),
        ("0114", "Bancaribe"),
        ("0115", "Exterior"),
        ("0116", "Occidental de Descuento"),
        ("0128", "Banco Caroní"),
        ("0134", "Banesco"),
        ("0138", "Banco Plaza"),
        ("0151", "BFC Banco Fondo Común"),
        ("0156", "100% Banco"),
        ("0157", "Del Sur"),
        ("0163", "Banco del Tesoro"),
        ("0166", "Banco Agrícola de Venezuela"),
        ("0168", "Bancrecer"),
        ("0169", "Mi Banco"),
        ("0171", "Banco Activo"),
        ("0172", "Bancamiga"),
        ("0174", "Banplus"),
        ("0175", "Bicentenario del Pueblo"),
        ("0177", "Banfanb"),
        ("0191", "BNC Nacional de Crédito"),
    ]

    bank = models.CharField(max_length=4, choices=BANKS, default="0172")

    request_body = models.JSONField()
