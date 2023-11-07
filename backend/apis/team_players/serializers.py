from django.urls import reverse
from rest_framework import serializers

from apps.teams.models import (
    Team,
)
from apis.game_schedule.serializers import SeasonInlineSerializer
from apps.public_pages.models import Season
from apps.teams.models import PlayerTeam

from .services import (
    get_player_team,
    get_player_team_2
)


class TeamPlayersOptionsSerializer(serializers.ModelSerializer):
    current_season = serializers.SerializerMethodField(read_only=True)
    seasons = serializers.SerializerMethodField(read_only=True)
    create_player_url = serializers.SerializerMethodField(read_only=True)
    players_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'current_season',
            'seasons',
            'id',
            'name',
            'division',
            'logo',
            'create_player_url',
            'players_url'
        ]
    
    def get_seasons(self, instance):
        seasons = Season.seasons.all()
        return SeasonInlineSerializer(seasons, many=True).data
    
    def get_current_season(self, instance):
        current = Season.seasons.all().first()
        return SeasonInlineSerializer(current).data
    
    def get_create_player_url(self, instance):
        return reverse(
            'team_players:create',
            args=(
                instance.get_division_display(),
                instance.slug
            )
        )
    
    def get_players_url(self, instance):
        return reverse(
            'team_players:all', 
            args=(
                instance.get_division_display(),
                instance.slug
            )
        )


class PlayerCreateSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    position = serializers.CharField()
    player_number = serializers.IntegerField()
    height_feet = serializers.IntegerField()
    height_inches = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    weight = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    season = serializers.IntegerField()

    def __init__(self, instance=None, data=..., **kwargs):
        self.team = kwargs['context'].pop('team', None)
        self.is_update = kwargs['context'].pop('is_update', False)
        self.player = kwargs['context'].pop('player', None)
        super().__init__(instance, data, **kwargs)

    def validate_player_number(self,value):
        season = self.initial_data.get('season', None)

        player_team = get_player_team(
            number=value,
            team=self.team,
            season=season
        )
        
        if self.is_update and not self._is_edited():
            return value

        if player_team is not None:
            raise serializers.ValidationError("Player with this number is already existing!")
        
        return value
    
    def _is_edited(self):
        player_number = self.initial_data.get('player_number', None)
        return self.player.number != int(player_number)


class PlayerTeamSerializer(serializers.ModelSerializer):
    last_name = serializers.SerializerMethodField(read_only=True)
    first_name = serializers.SerializerMethodField(read_only=True)
    height = serializers.SerializerMethodField(read_only=True)
    height_feet = serializers.SerializerMethodField(read_only=True)
    height_inches = serializers.SerializerMethodField(read_only=True)
    weight = serializers.SerializerMethodField(read_only=True)
    player_number = serializers.SerializerMethodField(read_only=True)
    fullname = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PlayerTeam
        fields = [
            'id',
            'first_name',
            'last_name',
            'player_number',
            'height',
            'height_feet',
            'height_inches',
            'weight',
            'position',
            'fullname'
        ]
    
    def get_last_name(self, instance):
        return instance.player.last_name
    
    def get_first_name(self, instance):
        return instance.player.first_name
    
    def get_height(self, instance):
        return instance.player.height
    
    def get_weight(self, instance):
        return instance.player.weight
    
    def get_height_feet(self, instance):
        return instance.player.height_feet
    
    def get_height_inches(self, instance):
        return instance.player.height_inches
    
    def get_player_number(self, instance):
        return instance.number

    def get_fullname(self, instance):
        return instance.player.full_name