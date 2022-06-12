from rest_framework import serializers
from accounts.serializers import UserSignUpSerializer
from .models import Transaction


class TransactionDetailSerializer(serializers.ModelSerializer):
    user = UserSignUpSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = (
            "user",
            "transaction_id",
            "transfer_to",
            "received_from",
            "amount",
            "not_pending",
            "is_credit",
            "done_on"
        )


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
