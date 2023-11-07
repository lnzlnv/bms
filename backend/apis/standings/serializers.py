from django.utils.text import slugify
from django.urls import reverse
from rest_framework import serializers

from apis.super_statistician.serializers_2 import StatsSerializer
from apis.teams.serializers import TeamSerializer
from apps.statisticians.models import (
    PlayerStat,
    TeamStat,
)
from apis.team_players.serializers import PlayerTeamSerializer


class TeamStatSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField(read_only=True)
    stat = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = TeamStat
        fields = [
            'id',
            'win',
            'lose',
            'team_win_percentage',
            'team',
            'games_played',
            'pts_per_game',
            'field_goal_made_per_game',
            'field_goals_att_per_game',
            'three_pts_made_per_game',
            'three_pts_att_per_game',
            'two_pts_made_per_game',
            'two_pts_att_per_game',
            'ft_made_per_game',
            'ft_att_per_game',
            'reb_off_per_game',
            'reb_def_per_game',
            'reb_per_game',
            'assists_per_game',
            'steals_per_game',
            'blocks_per_game',
            'turnovers_per_game',
            'stat'
        ]

    def __init__(self, instance=None, **kwargs):
        self.standing_type = kwargs['context'].pop('standing_type', None)
        super().__init__(instance, **kwargs)

    def get_stat(self, instance):
        return StatsSerializer(instance.stat).data

    def get_team(self, instance):
        if self.standing_type is None or self.standing_type == 'ELIMINATIONS':
            return TeamSerializer(instance.stat.team_season_stat.team).data
        
        if self.standing_type == 'PLAYOFFS':
            return TeamSerializer(instance.stat.team_playoffs_stat.team).data


class PlayerStatSerializer(serializers.ModelSerializer):
    team = serializers.SerializerMethodField(read_only=True)
    stat = serializers.SerializerMethodField(read_only=True)
    player_info = serializers.SerializerMethodField(read_only=True)
    info_page = serializers.SerializerMethodField(read_only=True)
    ppg_percentage = serializers.SerializerMethodField(read_only=True)
    rpg_percentage = serializers.SerializerMethodField(read_only=True)
    apg_percentage = serializers.SerializerMethodField(read_only=True)
    ftg_percentage = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PlayerStat
        fields = [
            'player_info',
            'games_played',
            'minutes_played',
            'pts_per_game',
            'field_goal_made_per_game',
            'field_goals_att_per_game',
            'three_pts_made_per_game',
            'three_pts_att_per_game',
            'two_pts_made_per_game',
            'two_pts_att_per_game',
            'ft_made_per_game',
            'ft_att_per_game',
            'ftp_per_game',
            'reb_off_per_game',
            'reb_def_per_game',
            'reb_per_game',
            'assists_per_game',
            'steals_per_game',
            'blocks_per_game',
            'turnovers_per_game',
            'team',
            'stat',
            'info_page',
            'ppg_percentage',
            'rpg_percentage',
            'apg_percentage',
            'ftg_percentage',
        ]

    def __init__(self, instance=None, **kwargs):
        self.is_list = type(instance) is list
        self.standing_type = kwargs['context'].pop('standing_type', None)

        super().__init__(instance, **kwargs)

    def get_stat(self, instance):
        return StatsSerializer(instance.stats).data

    def get_team(self, instance):
        player = self._get_player(instance)
        return TeamSerializer(player.team).data

    def get_player_info(self, instance):
        player = self._get_player(instance)
        return PlayerTeamSerializer(player).data

    def get_info_page(self, instance):
        player = self._get_player(instance)
        return reverse(
            'stats:single-player',
            args=(
                player.slug,
            )
        )

    def _get_player(self, instance):
        if self.standing_type == 'ELIMINATIONS' or self.standing_type is None:
            return instance.stats.player_season_stat.player_team
        if self.standing_type == 'PLAYOFFS':
            return instance.stats.player_playoffs_stat.player_team

    def get_ppg_percentage(self, instance):
        if self.is_list:
            return 0

        return instance.ppg_percentage

    def get_rpg_percentage(self, instance):
        if self.is_list:
            return 0

        return instance.rpg_percentage

    def get_apg_percentage(self, instance):
        if self.is_list:
            return 0

        return instance.apg_percentage

    def get_ftg_percentage(self, instance):
        if self.is_list:
            return 0

        return instance.ftg_percentage
