from rest_framework import serializers

from apps.authentication.models import User
from apps.public_pages.models import Season
from apis.game_schedule.services import get_image_name

class UserRequestSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'contact_number',
            'role',
            'status',
        ]
    
    def get_role(self, instance):
        return instance.get_user_role_display()


class SeasonSerializer(serializers.ModelSerializer):
    logo_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Season
        fields = [
            'id',
            'year',
            'logo',
            'logo_name'
        ]

    def get_logo_name(self, instance):
        return get_image_name(image=instance.logo.name)