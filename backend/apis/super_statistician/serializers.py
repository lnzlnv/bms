from django.urls import reverse
from rest_framework import serializers
from rest_framework.fields import empty

from apis.game_schedule.serializers import SeasonInlineSerializer
from apis.team_players.serializers import PlayerTeamSerializer
from apis.statisticians.serializers import PointsClassificationSerializer
from apps.authentication.models import User
from apps.public_pages.models import Season
from apps.teams.models import Team
from apps.game_schedule.models import (
    Game,
)
from apps.statisticians.models import (
    Stat,
    PlayerGameStat,
    TeamTimeStatsAnalysis,
    PointsInAQuarter,
    TeamGameStat
)
from .services import (
    get_points_classification
)
from .services_2 import get_time_analysis_data
from .selectors import get_points_in_a_quarter
from .serializers_2 import StatsSerializer



class PlayerGameStatSerializer(serializers.ModelSerializer):
    info = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    is_starter = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PlayerGameStat
        fields = [
            'info',
            'stats',
            'is_starter'
        ]

    def get_info(self, instance):
        return PlayerTeamSerializer(instance.player).data

    def get_stats(self, instance):
        return StatsSerializer(instance.stats).data
    
    def get_is_starter(self, instance):
        return instance.stats.player_stats.is_starter


class PointsInAQuarterSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointsInAQuarter
        fields = [
            'id',
            'quarter',
            'points'
        ]


class TeamSerializer(serializers.ModelSerializer):
    division_name = serializers.SerializerMethodField(read_only=True)
    logo_name = serializers.SerializerMethodField(read_only=True)
    players = serializers.SerializerMethodField(read_only=True)
    half_time_analysis = serializers.SerializerMethodField(read_only=True)
    full_time_analysis = serializers.SerializerMethodField(read_only=True)
    points_classification = serializers.SerializerMethodField(read_only=True)
    points_per_quarter = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'division',
            'logo',
            'division_name',
            'logo_name',
            'players',
            'half_time_analysis',
            'full_time_analysis',
            'points_classification',
            'points_per_quarter',
            'stats'
        ]

    def __init__(self, instance=None, **kwargs):
        self.game = kwargs.pop('game', None)
        super().__init__(instance, **kwargs)

    def get_division_name(self, instance):
        return instance.get_division_display()
    
    def get_logo_name(self, instance):
        name = instance.logo.name.split('/')[-1]
        return name

    def get_players(self, instance):
        players = instance.players.filter(
            season=self.game.season
        )
        players_stats = PlayerGameStat.player_game_stats.filter(
            player__in=players,
            game=self.game
        )

        return PlayerGameStatSerializer(players_stats, many=True).data

    def get_half_time_analysis(self, instance):
        return get_time_analysis_data(
            quarter=2,
            game_id=self.game.id,
            team=instance
        )

    def get_full_time_analysis(self, instance):
        game_quarter = self.game.quarter
        return get_time_analysis_data(
            quarter=game_quarter,
            game_id=self.game.id,
            team=instance
        )

    def get_points_classification(self, instance):
        classification = get_points_classification(
            game_id=self.game.id,
            team_id=instance.id,
        )
        return PointsClassificationSerializer(classification).data
    
    def get_points_per_quarter(self, instance):
        points = get_points_in_a_quarter(
            game_id=self.game.id,
            team_id=instance.id
        )
        return PointsInAQuarterSerializer(points, many=True).data
    
    def get_stats(self, instance):
        game_stat = TeamGameStat.stats.filter(
            game=self.game,
            team=instance.id
        ).first()

        if game_stat is None:
            return None

        return StatsSerializer(game_stat.stat).data

class GameStatsApprovalSerializer(serializers.ModelSerializer):
    seasons = serializers.SerializerMethodField(read_only=True)
    current_season = serializers.SerializerMethodField(read_only=True)
    divisions = serializers.SerializerMethodField(read_only=True)


    class Meta:
        model = User
        fields = [
            'seasons',
            'current_season',
            'divisions'
        ]
    
    def get_seasons(self, instance):
        seasons = Season.seasons.all()
        return SeasonInlineSerializer(seasons, many=True).data
    
    def get_current_season(self, instance):
        current = Season.seasons.all().first()
        return SeasonInlineSerializer(current).data
    
    def get_divisions(self, instance):
        return Team().DIVISIONS


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name'
        ]


class GameSerializer(serializers.ModelSerializer):
    home_team = serializers.SerializerMethodField(read_only=True)
    away_team = serializers.SerializerMethodField(read_only=True)
    reports_url = serializers.SerializerMethodField(read_only=True)
    season = serializers.SerializerMethodField(read_only=True)
    full_time_analysis_can_be_generated = \
        serializers.SerializerMethodField(read_only=True)
    approved_by_super_statistician = \
        serializers.SerializerMethodField(read_only=True)
    approved_by_admin = serializers.SerializerMethodField(read_only=True)
    game_type = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Game
        fields = [
            'id',
            'home_team',
            'away_team',
            'reports_url',
            'season',
            'has_half_time_analysis',
            'has_full_time_analysis',
            'player_stats_are_generated',
            'full_time_analysis_can_be_generated',
            'is_approved_by_super_statistician',
            'approved_by_super_statistician',
            'is_approved_by_admin',
            'approved_by_admin',
            'slug',
            'game_type'
        ]
    
    def get_home_team(self, instance):
        return TeamSerializer(
            instance.home_team,
            game=instance,
        ).data

    def get_away_team(self, instance):
        return TeamSerializer(
            instance.away_team,
            game=instance,
        ).data
    
    def get_reports_url(self, instance):
        return reverse(
            'super_statistician:stats-reports', 
            args=(instance.slug,)
        )
    
    def get_season(self, instance):
        return SeasonInlineSerializer(instance.season, ).data
    
    def get_full_time_analysis_can_be_generated(self, instance):
        return instance.quarter >= 4
    
    def get_approved_by_super_statistician(self, instance):
        return UserSerializer(instance.approved_by_super_statistician).data
    
    def get_approved_by_admin(self, instance):
        return UserSerializer(instance.approved_by_admin).data
    
    def get_game_type(self, instance):
        return {
            'value': instance.game_type,
            'name': instance.get_game_type_display()
        }