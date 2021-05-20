import logging

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token

logger = logging.getLogger("django")


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "password")

    def validate(self, attributes):
        logger.info("Generating password hash")
        attributes["password"] = make_password(attributes["password"])
        return attributes


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        "invalid_credentials": _("Unable to login with provided credentials.")
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attributes):
        logger.info("Validating user credentials")
        self.user = authenticate(
            username=attributes.get("username"), password=attributes.get("password")
        )
        if self.user:
            logger.info("Validated user credentials")
            return attributes
        else:
            logger.info("User credentials not valid")
            raise serializers.ValidationError(
                self.error_messages["invalid_credentials"]
            )


class TokenSerializer(serializers.ModelSerializer):
    auth_token = serializers.CharField(source="key")

    class Meta:
        model = Token
        fields = ("auth_token", "created")
