from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from accounts.models import User, UserDetail


class UserSignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password1 = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ("email", "name", "mobile_no", "password1", "password2")

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Passwords didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data["email"],
            name=validated_data["name"],
            mobile_no=validated_data["mobile_no"],
        )
        user.set_password(validated_data["password1"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    user = UserSignUpSerializer(read_only=True)

    class Meta:
        model = UserDetail
        fields = (
            "user",
            "age",
            "gender",
            "date_of_birth",
            "address",
            "aadhar_number",
            "pan_card",
            "account_balance"
        )


class UserDetailProfile(serializers.ModelSerializer):
    class Meta:
        model = UserDetail
        fields = "__all__"
