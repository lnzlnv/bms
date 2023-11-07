from rest_framework import serializers

from apps.authentication.models import User
from apps.teams.models import Team


class GamesForAdminApprovalOptionsSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'divisions'
        ]

    def get_divisions(self, instance):
        return Team().DIVISIONS