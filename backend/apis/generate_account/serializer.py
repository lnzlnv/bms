from rest_framework import serializers

from apps.authentication.models import User


class GenerateAccountSerializer(serializers.ModelSerializer):
    user_role_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'user_role',
            'user_role_name',
            'expiration_date',
            'username',
            'password',
            'password_raw',
            'first_name',
            'last_name'
        ]

    def get_user_role_name(self, instance):
        if not isinstance(instance, User):
            return ''

        return instance.get_user_role_display()
