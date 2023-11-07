import datetime

from django.db.models import F

from apps.game_schedule.models import (
    GameSchedule,
    Game
)
from apps.statisticians.models import (
    Stat,
    PlayerStat,
    PlayerGameStat,
    PointsClassification,
    Substitution,
    InGamePlayer,
    PointsInAQuarter,
    TeamTimeStatsAnalysis,
    TeamGameStat,
    PlayerTeam,
    OfficiateHistory
)
from apps.teams.models import (
    Player
)


class PlayerGameStats:
    def __init__(self, game) -> None:
        self.game = game
        self.season = game.season

    def create(self):
        self._create_player_stats(self.game.home_team.players.all())
        self._create_points_classification(self.game.home_team)

        self._create_player_stats(self.game.away_team.players.all())
        self._create_points_classification(self.game.away_team)

        self.game.player_stats_are_generated = True
        self.game.save()

    def _create_player_stats(self, players):
        for player in players:
            stats_type = 'P'
            stats = Stat.stats.create(stats_type=stats_type)
            PlayerStat.player_stats.create(
                stats=stats
            )
            PlayerGameStat.player_game_stats.create(
                player=player,
                game=self.game,
                stats=stats,
                season=self.season
            )

    def _create_points_classification(self, team):
        classification = PointsClassification.classifications.create(
            game=self.game,
            team=team
        )
        classification.save()


class TeamGameStats:
    def __init__(self, game) -> None:
        self.game = game
        self.season = game.season

    def create(self):
        self._create_team_game_stat(self.game.home_team)
        self._create_team_game_stat(self.game.away_team)

    def _create_team_game_stat(self, team):
        stat = Stat.stats.create(stats_type='TG')

        TeamGameStat.stats.create(
            season=self.season,
            game=self.game,
            team=team,
            stat=stat
        )


class Points:
    def __init__(self, game, team_id, validated_data, operation):
        quarter = validated_data['quarter']
        self.quarter = quarter if quarter <= 4 else 4
        self.game = game
        self.team_id = team_id
        self.validated_data = validated_data
        self.operation = operation

    def update_quarter_points(self):
        quarter = PointsInAQuarter.quarter_points.filter(
            game=self.game,
            team=self.team_id,
            quarter=self.quarter
        ).first()

        if self.operation == 'REDO':
            quarter.points = F('points') + self.validated_data['points']
            quarter.save()
            return

        quarter.points = F('points') - self.validated_data['points']
        quarter.save()


class ValidatedData:
    def __init__(self,
                 game_id,
                 team_id,
                 data,
                 validated_data,
                 stats: object,
                 operation='REDO'
                 ) -> None:
        self.classification = None
        self.data = data
        self.validated_data = validated_data
        self.stats = stats
        self.team_id = team_id
        self.game = Game.games.filter(pk=game_id).first()
        self.team_game_stats = TeamGameStat.stats.filter(
            game=game_id,
            team=team_id
        ).first()
        self.operation = operation

    def update(self):
        self.classification = self._get_classification()
        for (index, key) in enumerate(self.data):
            try:
                value = self.validated_data[key]
                self._update_player_game_stats(key, value)
                self._update_team_game_stats(key, value)
            except AttributeError:
                self._is_ejected(key)
                self._is_disqualified(key)
                self._is_point_off_turnover(key)
                self._is_point_fast_break(key)
                self._is_second_chance(key)

        self._is_bench_player()
        self._is_starter_player()
        self._is_update_points()

        self.team_game_stats.stat.save()

    def _get_classification(self):
        game_id = self.stats.player_game_stat.game.id
        team_id = self.stats.player_game_stat.player.team.id

        return PointsClassification.classifications.filter(
            game=game_id,
            team=team_id
        ).first()

    def _update_player_game_stats(self, key, value):
        if self.operation == 'REDO':
            self.validated_data[key] += getattr(self.stats, key)
            return
        self.validated_data[key] = getattr(self.stats, key) - value

    def _update_team_game_stats(self, key, value):
        if self.operation == 'REDO':
            new_value = value + F(key)
            setattr(self.team_game_stats.stat, key, new_value)
            return

        new_value = F(key) - value
        setattr(self.team_game_stats.stat, key, new_value)

    def _is_ejected(self, key):
        if key != 'ejected':
            return
        if self.operation == 'REDO':
            self.team_game_stats.stat.fouls = F('fouls') + self.stats.fouls
            self.validated_data['is_ejected'] = True
            return

        self.team_game_stats.stat.fouls = F('fouls') - self.stats.fouls
        self.validated_data['is_ejected'] = False

    def _is_disqualified(self, key):
        if key != 'disqualified':
            return

        if self.operation == 'REDO':
            self.team_game_stats.stat.fouls = F('fouls') + self.stats.fouls
            self.validated_data['is_disqualified'] = True
            return

        self.team_game_stats.stat.fouls = F('fouls') - self.stats.fouls
        self.validated_data['is_disqualified'] = False

    def _is_point_off_turnover(self, key):
        if key != 'off_turnover':
            return
        if self.operation == 'REDO':
            self.classification.off_turnover += self.validated_data['points']
            self.classification.save()
            return

        self.classification.off_turnover -= self.validated_data['points']
        self.classification.save()

    def _is_point_fast_break(self, key):
        if key != 'fast_break':
            return

        if self.operation == 'REDO':
            self.classification.fast_break += self.validated_data['points']
            self.classification.save()
            return

        self.classification.fast_break -= self.validated_data['points']
        self.classification.save()

    def _is_second_chance(self, key):
        if key != 'second_chance':
            return

        if self.operation == 'REDO':
            self.classification.second_chance += self.validated_data['points']
            self.classification.save()
            return

        self.classification.second_chance -= self.validated_data['points']
        self.classification.save()

    def _is_bench_player(self):
        if (self.stats.player_stats.is_starter
                or 'points' not in self.validated_data):
            return

        if self.operation == 'REDO':
            self.classification.bench += self.validated_data['points']
            self.classification.save()
            return

        self.classification.bench -= self.validated_data['points']
        self.classification.save()

    def _is_starter_player(self):
        if (not self.stats.player_stats.is_starter
                or 'points' not in self.validated_data):
            return

        if self.operation == 'REDO':
            self.classification.starters += self.validated_data['points']
            self.classification.save()
            return

        self.classification.starters -= self.validated_data['points']
        self.classification.save()

    def _is_update_points(self):
        if not ('points' in self.validated_data):
            return

        points = Points(
            game=self.game,
            team_id=self.team_id,
            validated_data=self.validated_data,
            operation=self.operation
        )

        points.update_quarter_points()


class SubstitutionTime:
    def __init__(self, data, game, team_id) -> None:
        self.isHomeTeam = game.home_team.id == team_id
        self.data = data
        self.sub_out_all = data['sub_out_all']
        self.game = game
        self.team = 'home_team' if self.isHomeTeam else 'away_team'
        self.subIn = self._get_player_list(data['sub_in'])
        self.subOut = self._get_player_list(data['sub_out'])

    def record(self):
        self._create_substitution_objects()
        self._create_in_game_player_object()
        self._update_in_game_players()

    def _create_substitution_objects(self):
        subIn = 'I'
        self._create(self.subIn, subIn)

        subOut = 'O'
        self._create(self.subOut, subOut)

    def _get_player_list(self, players):
        return players.split(' ')

    def _create(self, players, status):
        team = self._get_team(players)

        for index, player_number in enumerate(players):
            if player_number == '':
                continue

            if index >= 5:
                team = self.game.away_team

            Substitution.substitutions.create(
                player=self._get_player(player_number, team),
                game=self.game,
                minutes=self.data['minutes'],
                seconds=self.data['seconds'],
                status=status,
                quarter=self.data['quarter']
            )

    def _get_team(self, players):
        if self.isHomeTeam or len(players) == 10:
            return self.game.home_team

        return self.game.away_team

    def _get_player(self, player_number, team):
        return PlayerTeam.players.filter(
            number=player_number,
            team=team,
            season=self.game.season
        ).first()

    def _create_in_game_player_object(self):
        if self.game.in_game_players_are_generated:
            return

        self._create_in_game({f'{self.team}': self.subIn})

        self.game.in_game_players_are_generated = True
        self.game.save()

    def _create_in_game(self, team):
        InGamePlayer.players.create(
            game=self.game,
            **team
        )

    def _update_in_game_players(self):
        self.in_game_player = InGamePlayer.players.filter(game=self.game.id).first()
        if self.sub_out_all:
            self.in_game_player.away_team = []
            self.in_game_player.home_team = []
            self.in_game_player.save()
            MinutesPlayed(game=self.game).compute_both_team()
            return

        if self.isHomeTeam:
            self._update_in_game(self.in_game_player.home_team)
        else:
            self._update_in_game(self.in_game_player.away_team)

        self.in_game_player.save()

    def _update_in_game(self, team):
        for player_number in self.subOut:
            if player_number == '':
                continue

            if player_number in team:
                team.remove(player_number)

        for player_number in self.subIn:
            if player_number != '' and player_number not in team:
                team.append(player_number)


class PointsPerQuarter:
    def __init__(self, game, quarter) -> None:
        self.game = game
        self.quarter = quarter

    def set(self):
        is_new_quarter = self.game.quarter != self.quarter
        has_overtimes = self.quarter > 4

        if not is_new_quarter or has_overtimes:
            return

        self._create_object(self.game.home_team)
        self._create_object(self.game.away_team)

    def _create_object(self, team):
        PointsInAQuarter.quarter_points.create(
            game=self.game,
            team=team,
            quarter=self.quarter
        )


class StarterAndBenchPointsClassification:
    def __init__(self, team, game, player_stats) -> None:
        self.team = team
        self.game = game
        self.players_stats = player_stats

    def get_team_points_classification(self):
        self.classification_team = PointsClassification.classifications.filter(
            game=self.game,
            team=self.team,
        ).first()

        return self.classification_team

    def calculate_points(self):
        starters = 0
        bench = 0
        for stat in self.players_stats:
            if stat.player_stats.is_starter:
                starters += stat.total_points
            else:
                bench += stat.total_points

        self.classification_team.starters = starters
        self.classification_team.bench = bench
        self.classification_team.save()


class TeamStatsAnalysis:
    def __init__(self, game, quarter) -> None:
        self.game = game
        self.quarter = quarter

    def create(self):
        """Create analysis based on quarter"""
        self._create_team_analysis(self.game.home_team)
        self._create_team_analysis(self.game.away_team)

    def _create_team_analysis(self, team):
        self._set_player_stats(players=team.players.all())
        self._set_stat()
        self._update_starter_and_bench_of_team_points_classification(team)
        self._set_points_classification_for_analysis(team)
        self._set_time_analysis(team)
        self._calculate_analysis()
        self._set_analysis_points_classification(team)

    def _set_player_stats(self, players):
        self.players_stats = Stat.stats.filter(
            player_game_stat__game=self.game,
            player_game_stat__player__in=players
        )

    def _set_stat(self):
        timeStatType = 'TA'
        self.stat = Stat.stats.create(
            stats_type=timeStatType
        )

    def _update_starter_and_bench_of_team_points_classification(self, team):
        self.classification = StarterAndBenchPointsClassification(
            team=team,
            game=self.game,
            player_stats=self.players_stats
        )
        self.classification_team = \
            self.classification.get_team_points_classification()
        self.classification.calculate_points()

    def _set_points_classification_for_analysis(self, team):
        self.points_classification = \
            PointsClassification.classifications.create(
                game=self.game,
                team=team,
                is_time_analysis=True,
                quarter=self.quarter
            )

    def _set_time_analysis(self, team):
        self.time_analysis = TeamTimeStatsAnalysis.analyses.create(
            season=self.game.season,
            game=self.game,
            team=team,
            stat=self.stat,
            time=self.quarter,
            points_classification=self.points_classification
        )

    def _calculate_analysis(self):
        for stat in self.players_stats:
            self._add_field_value_to_team_stat(
                stat=stat,
                editable_fields=[
                    field.name
                    for field in stat._meta.fields
                    if field.editable
                ]
            )

        self.stat.save()

    def _add_field_value_to_team_stat(self, stat, editable_fields):
        for stat_field in editable_fields:
            if stat_field == 'id' or stat_field == 'stats_type':
                continue

            value = getattr(stat, stat_field) \
                    + getattr(self.stat, stat_field)

            setattr(self.stat, stat_field, value)

    def _set_analysis_points_classification(self, team):
        classification_analysis = PointsClassification.classifications.filter(
            game=self.game,
            team=team,
            is_time_analysis=True,
            quarter=self.quarter
        ).first()

        editable_fields = [
            field.name
            for field in self.classification_team._meta.fields
            if field.editable
        ]

        for field in editable_fields:
            if field == 'id':
                continue

            field_value = getattr(self.classification_team, field)
            setattr(classification_analysis, field, field_value)

        classification_analysis.save()


class MinutesPlayed:
    def __init__(self, game) -> None:
        self.game = game

    def compute_both_team(self):
        self.compute(self.game.home_team.players.filter(season=self.game.season))
        self.compute(self.game.away_team.players.filter(season=self.game.season))

    def compute(self, team_players):
        self._set_stats(team_players)

        for player in team_players:
            substitutions = Substitution.substitutions.filter(
                player=player.id,
                game=self.game
            )
            self.compute_minutes(player, substitutions)
            substitutions.delete()

    def _set_stats(self, team_players):
        self.players_stats = {}

        stats = Stat.stats.filter(
            player_game_stat__player__in=team_players
        )

        for stat in stats:
            self.players_stats[stat.player_game_stat.player.id] = stat

    def compute_minutes(self, player, substitutions):
        total_seconds = 0
        sub_in = None
        sub_out = None

        for time in substitutions:
            if time.is_sub_in:
                sub_in = (time.minutes * 60) + time.seconds

            if time.is_sub_out:
                sub_out = (time.minutes * 60) + time.seconds

            if sub_in is not None and sub_out is not None:
                total_seconds += (sub_in - sub_out)
                sub_in = None
                sub_out = None

        self.players_stats[player.id].player_stats.seconds_played = \
            F('seconds_played') + total_seconds
        self.players_stats[player.id].player_stats.save()


def get_todays_games_schedules():
    now = datetime.datetime.now()

    return GameSchedule.schedules.filter(
        date__date=now,
        game__is_finished=False
    )


def get_player(
        *,
        player_id: int
):
    return Player.players.filter(pk=player_id).first()


def update_game_quarter(
        *,
        game: Game,
        quarter: int
):
    game.quarter = quarter
    game.save()


def set_game_starters(
        *,
        game: Game
):
    inGamePlayers = InGamePlayer.players.filter(game=game.id).first()
    playersHome = PlayerGameStat.player_game_stats.filter(
        player__number__in=inGamePlayers.home_team,
        game=game,
        player__team=game.home_team
    )
    playersAway = PlayerGameStat.player_game_stats.filter(
        player__number__in=inGamePlayers.away_team,
        game=game,
        player__team=game.away_team
    )

    player_game_stats = playersHome.union(playersAway)

    for player_game_stat in player_game_stats:
        player_game_stat.stats.player_stats.is_starter = True
        player_game_stat.stats.player_stats.save()

    game.starters_are_set = True
    game.save()


def update_team_points_classification(
        *,
        game: object,
        team: object
):
    players = team.players.all()

    player_stats = Stat.stats.filter(
        player_game_stat__game=game,
        player_game_stat__player__in=players
    )

    classification = StarterAndBenchPointsClassification(
        team=team,
        game=game,
        player_stats=player_stats
    )

    classification.get_team_points_classification()
    classification.calculate_points()


def set_winner(
        *,
        game: Game
):
    home_stats = Stat.stats.filter(
        team_game_stat__game=game,
        team_game_stat__team=game.home_team
    ).first()

    away_stats = Stat.stats.filter(
        team_game_stat__game=game,
        team_game_stat__team=game.away_team
    ).first()

    if home_stats.total_points == away_stats.total_points:
        return

    if home_stats.total_points > away_stats.total_points:
        game.winner = game.home_team
    else:
        game.winner = game.away_team


def delete_officiate_history(
    game: int or object,
    statistician: int or object
):
    OfficiateHistory.histories.filter(
        game=game,
        statistician=statistician
    ).delete()