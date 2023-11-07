from rest_framework import serializers

from apis.admin.serializers import SeasonSerializer
from apis.game_schedule.services import get_current_season
from apps.authentication.models import User
from apps.public_pages.models import Season


class PlayersPublicOptionsSerializer(serializers.ModelSerializer):
	current_season = serializers.SerializerMethodField(read_only=True)
	seasons = serializers.SerializerMethodField(read_only=True)

	class Meta:
		model = User
		fields = [
			'current_season',
			'seasons'
		]

	def get_current_season(self, instance):
		serializer = SeasonSerializer(get_current_season())
		return serializer.data

	def get_seasons(self, instance):
		serializer = SeasonSerializer(Season.seasons.all(), many=True)
		return serializer.data
