from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import empty

from apps.teams.models import Team
from apps.authentication.models import User
from apps.public_pages.models import ScheduleBanner
from apps.game_schedule.models import (
    GameSchedule,
    Season
)
from apis.statisticians.serializers import TeamSerializer

from .services import (
    get_image_name,
    get_team,
    get_formatted_date,
    get_formatted_date_2
)

class TeamInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id',
            'name',
        ]


class SeasonYearSerializer(serializers.Serializer):
    year = serializers.IntegerField()


class CurrentSeasonSerializer(serializers.ModelSerializer):
    seasons = serializers.SerializerMethodField(read_only=True)
    current_season = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'seasons',
            'current_season',
        ]
    
    def get_seasons(self, instance):
        seasons = Season.seasons.all()
        return SeasonInlineSerializer(seasons, many=True).data
    
    def get_current_season(self, instance):
        current = Season.seasons.all().first()
        return SeasonInlineSerializer(current).data
    

class SeasonInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Season
        fields = [
            'id',
            'year',
            'logo'
        ]


class GameScheduleOptionsSerializer(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField(read_only=True)
    junior_division_teams = serializers.SerializerMethodField(read_only=True)
    senior_division_teams = serializers.SerializerMethodField(read_only=True)
    season = serializers.SerializerMethodField(read_only=True)
    seasons = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = [
            'divisions',
            'junior_division_teams',
            'senior_division_teams',
            'season',
            'seasons'
        ]

    def __init__(self, instance=None, data=None, **kwargs):
        self.seasons = Season.seasons.all()
        season = self.seasons.filter(pk=kwargs.pop('season', 0)).first()
        current_season = self.seasons[0]
        self.season = current_season if season is None else season
        super().__init__(instance,**kwargs)

    def get_divisions(self, instance):
        return Team().DIVISIONS
    
    def get_junior_division_teams(self, instance):
        junior_team = Team.teams.filter(
            division='J',
            participated_season__season=self.season.id
        )
        return TeamInlineSerializer(junior_team, many=True).data

    def get_senior_division_teams(self, instance):
        senior_team = Team.teams.filter(
            division='S',
            participated_season__season=self.season.id
        )
        return TeamInlineSerializer(senior_team, many=True).data
    
    def get_season(self, instance):
        return SeasonInlineSerializer(self.season).data
    
    def get_seasons(self, instance):
        return SeasonInlineSerializer(self.seasons, many=True).data


class GameScheduleSerializer(serializers.Serializer):
    division = serializers.CharField()
    home_team = serializers.IntegerField()
    away_team = serializers.IntegerField()
    season = serializers.IntegerField()
    date = serializers.DateTimeField()
    venue = serializers.CharField()
    game_type = serializers.CharField()


class GameScheduleEditSerializer(serializers.Serializer):
    division = serializers.CharField()

    home_team_id = serializers.IntegerField()
    away_team_id = serializers.IntegerField()
    
    home_team = serializers.SerializerMethodField(read_only=True)
    away_team = serializers.SerializerMethodField(read_only=True)
    
    season = serializers.IntegerField()
    venue = serializers.CharField()

    date_local = serializers.DateTimeField()

    date = serializers.SerializerMethodField(read_only=True)
    date_format = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)

    match = serializers.SerializerMethodField(read_only=True)
    game_type = serializers.CharField()

    def get_home_team(self, instance):
        home = get_team(team=instance['home_team_id'])
        serializers = TeamInlineSerializer(home)
        return serializers.data
        
    
    def get_away_team(self, instance):
        away = get_team(team=instance['away_team_id'])
        serializers = TeamInlineSerializer(away)
        return serializers.data
    
    def get_date_format(self, instance):
        date = instance['date_local']
        return date.strftime("%B %d, %Y")
    
    def get_time(self, instance):
        date = instance['date_local']
        return date.strftime("%I:%M %p")
    
    def get_date(self, instance):
        date = instance['date_local']
        return date.strftime("%Y-%m-%dT%H:%M")
    
    def get_match(self, instance):
        home = get_team(team=instance['home_team_id'])
        away = get_team(team=instance['away_team_id'])
        
        home_name = home.name if home is not None else ''
        away_name = away.name if away is not None else ''

        return '{} vs {}'.format(
            home_name,
            away_name
        )

    
class GameScheduleModelSerializer(serializers.ModelSerializer):
    date_format = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    date = serializers.SerializerMethodField(read_only=True)
    season = serializers.SerializerMethodField(read_only=True)
    home_team = serializers.SerializerMethodField(read_only=True)
    away_team = serializers.SerializerMethodField(read_only=True)
    game_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GameSchedule
        fields = [
            'id',
            'creator',
            'season',
            'date',
            'date_format',
            'division',
            'venue',
            'match',
            'time',
            'home_team',
            'away_team',
            'game_type'
        ]
    
    def get_date_format(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime("%B %d, %Y")

    def get_time(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime("%I:%M %p")
    
    def get_creator(self, instance):
        if instance.creator is None:
            return ''

        return instance.creator.last_name
    
    def get_date(self, instance):
        return get_formatted_date(date=instance.date)
    
    def get_season(self, instance):
        return instance.season.id
    
    def get_home_team(self, instance):
        serializer = TeamSerializer(instance.game.home_team)
        return serializer.data

    def get_away_team(self, instance):
        serializer = TeamSerializer(instance.game.away_team)
        return serializer.data
    
    def get_game_type(self, instance):
        return instance.game.game_type


class ScheduleBannerSerializer(serializers.ModelSerializer):
    season_name = serializers.SerializerMethodField(read_only=True)
    date_format = serializers.SerializerMethodField(read_only=True)
    division_name = serializers.SerializerMethodField(read_only=True)
    creator = serializers.SerializerMethodField(read_only=True)
    image_name = serializers.SerializerMethodField(read_only=True)
    date_format_2 = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ScheduleBanner
        fields = [
            'id',
            'season',
            'division',
            'date',
            'time',
            'image',
            'image_name',
            'season_name',
            'date_format',
            'date_format_2',
            'division_name',
            'creator'
        ]
    
    def get_season_name(self, instance):
        return instance.season.year
    
    def get_date_format(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime("%B %d, %Y")
    
    def get_division_name(self, instance):
        return instance.get_division_display()
    
    def get_creator(self, instance):
        if instance.creator:
            return instance.creator.last_name
    
    def get_image_name(self, instance):
        return get_image_name(image=instance.image.name)
    
    def get_date_format_2(self ,instance):
        return get_formatted_date(date=instance.date)
    
    def get_time(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime("%I:%M %p")


class ScheduleBannerModelSerializer(serializers.ModelSerializer):
    date_format = serializers.SerializerMethodField(read_only=True)
    date_format_2 = serializers.SerializerMethodField(read_only=True)
    division_name = serializers.SerializerMethodField(read_only=True)
    creator  = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ScheduleBanner
        fields = [
            'id',
            'season',
            'division',
            'division_name',
            'date',
            'date_format',
            'date_format_2',
            'image',
            'creator',
            'time'
        ]
    
    def get_time(self, instance):
        date = get_formatted_date_2(date=instance.date)
        return date.strftime("%I:%M %p")
    
    def get_date_format(self, instance):
        return instance.date.strftime("%B %d, %Y")
    
    def get_date_format_2(self ,instance):
        return get_formatted_date_2(date=instance.date)
    
    def get_division_name(self, instance):
        return instance.get_division_display()
    
    def get_creator(self, instance):
        if instance.creator:
            return instance.creator.last_name


class ScheduleBannerOptionSerializer(serializers.ModelSerializer):
    current_season = serializers.SerializerMethodField(read_only=True)
    seasons = serializers.SerializerMethodField(read_only=True)
    divisions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'current_season',
            'seasons',
            'divisions'
        ]
    
    def get_seasons(self, instance):
        seasons = Season.seasons.all()
        return SeasonInlineSerializer(seasons, many=True).data
    
    def get_divisions(self, instance):
        return Team().DIVISIONS
    
    def get_current_season(self, instance):
        current = Season.seasons.all().first()
        return SeasonInlineSerializer(current).data