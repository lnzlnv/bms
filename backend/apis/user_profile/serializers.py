from rest_framework import serializers
from django.contrib.auth import password_validation

from apps.authentication.models import User


class UserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(
        max_length=100,
        write_only=True
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'password',
            'password1',
            'first_name',
            'last_name'
        ]

    def validate_password1(self, value):
        password_validation.validate_password(value)
        return value
