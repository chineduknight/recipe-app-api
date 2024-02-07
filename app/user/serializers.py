"""
Serializers for the user API View.
"""
import re
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from django.utils.translation import gettext as _

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def validate_password(self, value):
        """
        Validate that the password is strong.
        - At least 8 characters long
        - Contains at least one digit
        - Contains at least one uppercase letter
        - Contains at least one lowercase letter
        - Contains at least one special character
        """
        if not re.findall('\d', value):
            raise serializers.ValidationError('Password must contain at least one digit.')
        if not re.findall('[A-Z]', value):
            raise serializers.ValidationError('Password must contain at least one uppercase letter.')
        if not re.findall('[a-z]', value):
            raise serializers.ValidationError('Password must contain at least one lowercase letter.')
        if not re.findall('[^a-zA-Z0-9]', value):
            raise serializers.ValidationError('Password must contain at least one special character.')
        return value


    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop("password", None)
        # call the original update method
        # we don't need to override everything
        user = super().update(instance, validated_data)

        # Only do so if password is passed
        if password:
            user.set_password(password) # Again this hashes the password
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user."""
        email = attrs.get("email")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
