"""Operation serializer"""

from django.db.models import Q

# DRF
from rest_framework import serializers

# Model
from wifi_zones_api.operations.models import Operation, Recharge, Payment, Transfer


class OperationListModelSerializer(serializers.ModelSerializer):
    """Operations list model serializer"""

    amount = serializers.SerializerMethodField()

    class Meta:
        model = Operation
        fields = ["id", "operation_type", "prev_balance", "post_balance", "amount", "created", "code"]

    def get_amount(self, obj: Operation) -> int:
        if obj.operation_type == "R":
            recharge = Recharge.objects.get(operation=obj.pk)
            return recharge.amount
        elif obj.operation_type == "P":
            payment = Payment.objects.get(operation=obj.pk)
            return payment.amount
        elif obj.operation_type == "T":
            transfer = Transfer.objects.get(Q(sender_operation=obj.pk) | Q(receiver_operation=obj.pk))
            return transfer.amount

        return 0
