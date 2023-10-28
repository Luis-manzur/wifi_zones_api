"""Transfers serializers"""

# Utils

# Django
from django.utils.translation import gettext_lazy as _

# Django REST Framework
from rest_framework import serializers

# Models
from wifi_zones_api.operations.models import Transfer, Operation
from wifi_zones_api.users.models import User


# Utilities


class TransferCreateModelSerializer(serializers.ModelSerializer):
    """Transfer create model serializer."""

    sender = serializers.HiddenField(default=serializers.CurrentUserDefault())
    receiver = serializers.SlugRelatedField(
        slug_field="username", queryset=User.objects.filter(is_client=True, is_active=True, is_verified=True)
    )

    class Meta:
        model = Transfer
        exclude = ["modified", "created", "receiver_operation", "sender_operation"]

    def validate(self, data):
        # validate sender transfer
        sender: User = data["sender"]

        if sender.balance <= data["amount"]:
            raise serializers.ValidationError(_("Insufficient funds"))

        return data

    def create(self, data):
        # Create sender operation
        sender_operation = Operation()
        sender_operation.user = data["sender"]
        sender_operation.operation_type = "T"
        sender_operation.prev_balance = sender_operation.user.balance
        sender_operation.post_balance = sender_operation.user.balance - data["amount"]
        sender_operation.save()

        # Create receiver operation
        receiver_operation = Operation()
        receiver_operation.user = data["receiver"]
        receiver_operation.operation_type = "T"
        receiver_operation.prev_balance = receiver_operation.user.balance
        receiver_operation.post_balance = receiver_operation.user.balance + data["amount"]
        receiver_operation.save()

        # Save transfer
        transfer = Transfer(**data)
        transfer.receiver_operation = receiver_operation
        transfer.sender_operation = sender_operation
        transfer.save()

        return data
