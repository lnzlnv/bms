from rest_framework import serializers
from django.urls import reverse
from rest_framework.fields import empty

from apps.game_schedule.models import (
    GameSchedule,
    Game
)
from apis.admin.serializers import SeasonSerializer
from apps.teams.models import (
    Team,
    PlayerTeam
)
from apps.authentication.models import User
from apis.game_schedule.services import (
    get_formatted_date,
)
from apps.statisticians.models import (
    Stat,
    PlayerGameStat,
    PointsClassification,
    InGamePlayer,
    TeamGameStat
)


class PointsClassificationSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField()
    class Meta:
        model = PointsClassification
        fields = [
            'id',
            'game',
            'team',
            'off_turnover',
            'fast_break',
            'second_chance',
            'starters',
            'bench'
        ]
    
    def get_team(self, instance):
        return instance.team.id


class StatsSerializer(serializers.ModelSerializer):
    is_starter = serializers.SerializerMethodField(read_only=True)
    minutes_played = serializers.SerializerMethodField(default=0)
    off_turnover = serializers.BooleanField(default=False)
    fast_break = serializers.BooleanField(default=False)
    second_chance = serializers.BooleanField(default=False)
    ejected = serializers.BooleanField(default=False)
    disqualified = serializers.BooleanField(default=False)
    points = serializers.IntegerField(default=0)
    quarter = serializers.IntegerField(default=0)

    class Meta:
        model = Stat
        fields = [
            'id',
            'stats_type',
            'two_pts_att',
            'two_pts_made',
            'two_pts_percentage',
            'three_pts_att',
            'three_pts_made',
            'three_pts_percentage',
            'total_att',
            'total_made',
            'total_fg_percentage',
            'ft_att',
            'ft_made',
            'ft_percentage',
            'reb_off',
            'reb_def',
            'reb_total',
            'assists',
            'steals',
            'blocks',
            'turnovers',
            'total_shots_att',
            'total_shots_made',
            'total_shots_percentage',
            'total_points',
            'is_starter',
            'minutes_played',
            'fouls',
            'is_ejected',
            'is_disqualified',
            'off_turnover',
            'fast_break',
            'second_chance',
            'ejected',
            'points',
            'quarter',
            'disqualified'
        ]

    def get_is_starter(self, instance):
        if type(instance) != Stat or not instance.is_player:
            return None
        
        is_player = instance.stats_type == 'P'
        if not is_player:
            return None
        
        return instance.player_stats.is_starter
    
    def get_minutes_played(self, instance):
        if type(instance) != Stat or not instance.is_player:
            return None
        
        is_player = instance.stats_type == 'P'
        if not is_player:
            return None
        
        return instance.player_stats.minutes_played




class PlayerTeamSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(read_only=True)
    player_id = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = PlayerTeam
        fields = [
            'id',
            'number',
            'name',
            'player_id',
            'stats'
        ]

    def __init__(self, instance=None, data=..., **kwargs):
        self.game_id = kwargs.pop('game', None)
        super().__init__(instance, **kwargs)

    def get_name(self, instance):
        first_name = instance.player.first_name.split(' ')

        initial = ''

        for name in first_name:
            initial += name[0].upper()

        return '{} {}'.format(
            initial,
            instance.player.last_name
        )
    
    def get_player_id(self, instance):
        return instance.player.id
    
    def get_stats(self, instance):
        players_stats = PlayerGameStat.player_game_stats.filter(
            player=instance.id,
            game=self.game_id
        ).first()

        if players_stats is None:
            return None
        
        return StatsSerializer(players_stats.stats).data
    


class TeamSerializer(serializers.ModelSerializer):
    players = serializers.SerializerMethodField(read_only=True)
    points_classification = serializers.SerializerMethodField(read_only=True)
    stats = serializers.SerializerMethodField(read_only=True)
    division = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'logo',
            'logo_name',
            'players',
            'division',
            'points_classification',
            'stats'
        ]

    def __init__(self, instance=None, data=..., **kwargs):
        self.game = kwargs.pop('game', None)
        super().__init__(instance, **kwargs)
    
    def get_players(self, instance):
        if self.game is None:
            return None

        players = instance.players.filter(
            season=self.game.season
        ).order_by('number')
        return PlayerTeamSerializer(
            players,
            many=True,
            game=self.game
        ).data
    
    def get_points_classification(self, instance):
        classification = PointsClassification.classifications.filter(
            game=self.game,
            team=instance.id
        ).first()
        serializer = PointsClassificationSerializer(classification)
        return serializer.data
    
    def get_stats(self, instance):
        if self.game is None:
            return None

        game_stat = TeamGameStat.stats.filter(
            game=self.game,
            team=instance.id
        ).first()

        return StatsSerializer(game_stat.stat).data

    def get_division(self, instance):
        return instance.get_division_display()


class GamesTodayOptions(serializers.ModelSerializer):
    divisions = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = User
        fields = [
            'divisions'
        ]

    def get_divisions(self, instance):
        return Team().DIVISIONS


class GameScheduleSerializer(serializers.ModelSerializer):
    season = serializers.SerializerMethodField(read_only=True)
    home_team = serializers.SerializerMethodField(read_only=True)
    away_team = serializers.SerializerMethodField(read_only=True)
    division = serializers.SerializerMethodField(read_only=True)
    time = serializers.SerializerMethodField(read_only=True)
    date_format_1 = serializers.SerializerMethodField(read_only=True)
    officiate_url = serializers.SerializerMethodField(read_only=True)
    reports_url = serializers.SerializerMethodField(read_only=True)
    is_approved_by_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = GameSchedule
        fields = [
            'id',
            'date',
            'division',
            'venue',
            'time',
            'season',
            'home_team',
            'away_team',
            'date_format_1',
            'officiate_url',
            'reports_url',
            'is_approved_by_admin'
        ]
    
    def get_season(self, instance):
        return SeasonSerializer(instance.season).data
    
    def get_home_team(self, instance):
        return TeamSerializer(instance.game.home_team).data
    
    def get_away_team(self, instance):
        return TeamSerializer(instance.game.away_team).data
    
    def get_division(self, instance):
        return instance.get_division_display()
    
    def get_time(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime('%I:%M %p')
    
    def get_date_format_1(self, instance):
        date = get_formatted_date(date=instance.date)
        return date.strftime('%B %d, %Y')
    
    def get_officiate_url(self, instance):
        return reverse(
            'statisticians:officiate-game',
            args=(instance.game.slug,)
        )
    
    def get_reports_url(self, instance):
        return reverse(
            'super_statistician:stats-reports', 
            args=(instance.game.slug,)
        )
    
    def get_is_approved_by_admin(self, instance):
        return instance.game.is_approved_by_admin


class InGamePlayersSerializer(serializers.ModelSerializer):
    home_team = serializers.SerializerMethodField(read_only=True)
    away_team = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InGamePlayer
        fields = [
            'home_team',
            'away_team'
        ]

    def get_home_team(self, instance):
        return instance.home_team

    def get_away_team(self, instance):
        return instance.away_team


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
    in_game_players = serializers.SerializerMethodField(read_only=True)
    admin_report_url = serializers.SerializerMethodField(read_only=True)
    has_game_winner = serializers.SerializerMethodField(read_only=True)
    game_type = serializers.SerializerMethodField(read_only=True)
    date_format_1 = serializers.SerializerMethodField(read_only=True)
    statistician = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Game
        fields = [
            'id',
            'home_team',
            'away_team',
            'in_game_players',
            'quarter',
            'admin_report_url',
            'has_game_winner',
            'game_type',
            'slug',
            'date_format_1',
            'statistician'
        ]

    def __init__(self, instance=None, **kwargs):
        self.user = kwargs['context'].pop('statistician', None)
        super().__init__(instance, **kwargs)
    
    def get_home_team(self, instance):
        return TeamSerializer(
            instance.home_team,
            game=instance
        ).data

    def get_away_team(self, instance):
        return TeamSerializer(
            instance.away_team,
            game=instance
        ).data
    
    def get_in_game_players(self, instance):
        if not hasattr(instance, 'in_game_players'):
            return

        return InGamePlayersSerializer(
            instance.in_game_players
        ).data
    
    def get_admin_report_url(self, instance):
        return reverse(
            'games_for_admin_approval:reports',
            kwargs={
                'game': instance.slug
            }
        )
    
    def get_has_game_winner(self, instance):
        return instance.winner is not None
    
    def get_game_type(self, instance):
        return instance.get_game_type_display()
    
    def get_date_format_1(self, instance):
        return get_formatted_date(
            date=instance.schedule.date
        ).strftime('%B %d, %Y')
    
    def get_statistician(self, instance):
        return UserSerializer(self.user).data

class SubstitutionSerializer(serializers.Serializer):
    sub_in = serializers.CharField(
        default='',
        required=False,
        allow_blank=True
    )
    sub_out = serializers.CharField(
        default='',
        required=False,
        allow_blank=True
    )
    minutes = serializers.IntegerField()
    seconds = serializers.IntegerField()
    sub_out_all = serializers.BooleanField(default=False)
    quarter = serializers.IntegerField()


class QuarterSerializer(serializers.Serializer):
    quarter = serializers.IntegerField()