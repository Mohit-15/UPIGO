from rest_framework import serializers
from accounts.serializers import UserSignUpSerializer
from .models import UPI


class UpiDetailSerializer(serializers.ModelSerializer):
    username = UserSignUpSerializer(read_only=True)

    class Meta:
        model = UPI
        fields = (
            "username",
            "upi_id",
            "created_at",
            "updated_at",
            "scan_code",
            "is_active"
        )


class UpiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UPI
        fields = "__all__"
