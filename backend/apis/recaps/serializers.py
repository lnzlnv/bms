from rest_framework import serializers

from apis.statisticians.serializers import GameSerializer

from apps.game_schedule.models import (
    Game,
    GameSchedule
)


class GameScheduleDateSerializer(serializers.ModelSerializer):
    games = serializers.SerializerMethodField(read_only=True)
    formatted_date = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = GameSchedule
        fields = [
            'date',
            'games',
            'venue',
            'formatted_date'
        ]

    def get_games(self, instance):
        games_in_given_date = Game.games.filter(
            schedule__date__date=instance.date.strftime('%Y-%m-%d')
        )

        return GameSerializer(games_in_given_date, many=True).data

    def get_formatted_date(self, instance):
        return instance.date.strftime('%a %b %d')


