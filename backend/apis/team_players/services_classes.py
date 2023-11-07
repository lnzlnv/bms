from rest_framework import serializers

from apps.teams.models import (
    PlayerTeam,
)
from apps.statisticians.models import (
    PlayerSeasonStat,
    Stat,
    PlayerStat
)

from .selectors import normalize_query
from .serializers import PlayerCreateSerializer
from .services import get_team, get_season_2


class Players:
    def __init__(self, kwargs, data):
        self.team = get_team(team=kwargs['team'])
        self.season = get_season_2(season_id=kwargs['season'])
        self.new_players_team = []
        player_ids = data['players'].split(',')
        self.players_team = normalize_query(
            query=PlayerTeam.players.filter(pk__in=player_ids)
        )
        self.data = data
        self.has_errors = False
        self.errors = {}
        self.context = {'team': self.team}
        self.players = []
        self.stats = []
        self.player_stats = []
        self.player_season_stats = []

    def validate_data(self):
        for player in self.players_team:
            data = self._get_data(player)
            has_error = False
            serializer = self._get_serializer(data)

            try:
                serializer.is_valid(raise_exception=True)
            except serializers.ValidationError as err:
                self.errors[player] = err.detail
                self.has_errors = True
                has_error = True

            if not has_error:
                self._add_to_new_players(
                    validated_data=serializer.validated_data,
                    player=player
                )

    def perform_create(self):
        for player_info in self.new_players_team:
            player_team = PlayerTeam(
                player=self.players_team[player_info['id']].player,
                team=self.team,
                season=self.season,
                position=player_info['position'],
                number=player_info['player_number']
            )
            stat = Stat(stats_type='PS')  # Player Season Type
            player_stat = PlayerStat(stats=stat)
            player_season_stat = PlayerSeasonStat(
                season=self.season,
                player_team=player_team,
                stat=stat
            )

            self.players.append(player_team)
            self.stats.append(stat)
            self.player_stats.append(player_stat)
            self.player_season_stats.append(player_season_stat)

        self._create_instances()

    def _create_instances(self):
        PlayerTeam.players.bulk_create(self.players)
        Stat.stats.bulk_create(self.stats)
        PlayerStat.player_stats.bulk_create(self.player_stats)
        PlayerSeasonStat.stats.bulk_create(self.player_season_stats)



    def _get_data(self, player_id):
        return {
            'season': self.season.year,
            'player_number': self.data['player-number-{}'.format(player_id)],
            'position': self.data['player-position-{}'.format(player_id)],
        }

    def _get_serializer(self, data):
        return PlayerCreateSerializer(
            data=data,
            partial=True,
            context=self.context
        )

    def _add_to_new_players(self, validated_data, player):
        self.new_players_team.append({
            'position': validated_data['position'],
            'player_number': validated_data['player_number'],
            'id': player
        })
