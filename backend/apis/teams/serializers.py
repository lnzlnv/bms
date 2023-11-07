from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import empty

from apis.game_schedule.serializers import SeasonInlineSerializer
from apps.public_pages.models import Season
from apps.authentication.models import User
from apps.teams.models import (
    Team,
    SeasonTeam
)


class CreateOptionsSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField(read_only=True)
    seasons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'seasons',
            'divisions'
        ]
    
    def get_divisions(self, instance):
        return Team().DIVISIONS

    def get_seasons(self, instance):
        seasons = Season.seasons.all()
        return SeasonInlineSerializer(seasons, many=True).data


class TeamSerializer(serializers.ModelSerializer):
    division_name = serializers.SerializerMethodField(read_only=True)
    logo_name = serializers.SerializerMethodField(read_only=True)
    players_url = serializers.SerializerMethodField(read_only=True)
    season_team = serializers.SerializerMethodField(read_only=True)
    season = serializers.IntegerField(write_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'division',
            'logo',
            'division_name',
            'logo_name',
            'players_url',
            'season_team',
            'season'
        ]

    def __init__(self, instance=None, **kwargs):
        self.season = kwargs['context'].pop('season', None) if 'context' in kwargs else None
        super().__init__(instance, **kwargs)

    def validate_season(self, value):
        if value == '':
            raise serializers.ValidationError('This field cannot be blank.')
        season = Season.seasons.filter(
            year=value
        ).first

        if season is None:
            raise serializers.ValidationError('Invalid. Make sure the value is a valid season.')

        return value


    def get_division_name(self, instance):
        return instance.get_division_display()
    
    def get_logo_name(self, instance):
        name = instance.logo.name.split('/')[-1]
        return name
    
    def get_players_url(self, instance):
        return reverse(
            'team_players:all', 
            args=(
                instance.get_division_display(), 
                instance.slug
            )
        )
    
    def get_season_team(self, instance):
        if self.season is None:
            return
        
        season_team = SeasonTeam.teams.filter(
            team=instance,
            season=self.season
        ).first()
        return season_team.id


class ImportPlayerSerializer(serializers.Serializer):
    teams = serializers.ListField(child=serializers.IntegerField())