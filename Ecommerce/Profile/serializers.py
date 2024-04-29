from rest_framework import serializers

from .models import User, Profile

# Serializers


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
        }


# Find Accout Serializer
class FindAccount(serializers.Serializer):
    email = serializers.EmailField()


# Reset Password Serializer
class ResetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )


# Profile Serializer
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            "url",
            "id",
            "user",
            "username",
            "email",
            "first_name",
            "last_name",
            "address",
            "state",
            "city",
            "zipcode",
            "landmark",
            "contact_no",
            "created_on",
        ]
        extra_kwargs = {
            "user": {"read_only": True},
        }
