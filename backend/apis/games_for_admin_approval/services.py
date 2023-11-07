from apps.statisticians.models import (
    PlayerStat,
    Stat,
    TeamPlayoffsStat,
    PlayerPlayoffsStat,
    TeamStat,
)
from apps.teams.models import (
    SeasonTeam,
)


class PlayerSeasonStatComputation:
    def __init__(self, game):
        self.game = game

    def compute_both_teams(self):
        if self.game.is_finals:
            return
        
        self.compute(self.game.home_team)
        self.compute(self.game.away_team)

    def compute(self, team):
        self._set_players(team)
        self._set_consolidated_stats_query()
        self._set_game_stats_query()
        self._set_game_stats()
        self._set_consolidated_stats()
        self._set_editable_fields()
        self._perform_computation()

    def _set_players(self, team):
        self.players = team.players.filter(
            season=self.game.season
        )

    def _set_consolidated_stats_query(self):
        if self.game.is_eliminations:
            self.consolidated_stats_query = Stat.stats.filter(
                player_season_stat__player_team__in=self.players
            )
        elif self.game.is_playoffs:
            self.consolidated_stats_query = Stat.stats.filter(
                player_playoffs_stat__player_team__in=self.players
            )
        else:  # do nothing
            pass

    def _set_game_stats_query(self):
        self.game_stats_query = Stat.stats.filter(
            player_game_stat__player__in=self.players,
            player_game_stat__game=self.game
        )

    def _set_game_stats(self):
        self.game_stats = self._normalize_query(
            query=self.game_stats_query,
            stat_type='game'
        )

    def _set_consolidated_stats(self):
        self.consolidated_stats = self._normalize_query(
            query=self.consolidated_stats_query,
            stat_type='season'
        )

    def _normalize_query(self, query, stat_type):
        normalize = {}

        for data in query:
            if stat_type == 'game':  # game stat
                self._game(normalize, data)
            elif stat_type == 'season':  # season stat
                self._season(normalize, data)
        return normalize

    def _game(self, container, data):
        container[data.player_game_stat.player.id] = data

    def _season(self, container, data):
        if self.game.is_eliminations:
            container[data.player_season_stat.player_team.id] = data
        elif self.game.is_playoffs:
            container[data.player_playoffs_stat.player_team.id] = data
        else:  # do nothing
            pass

    def _set_editable_fields(self):
        self.stat_editable_fields = get_editable_fields(
            instance=self.game_stats[self.players[0].id]
        )

    def _perform_computation(self):
        updated_season_stats = []
        updated_player_stats = []

        for player in self.players:
            games_played_is_updated = False

            for field in self.stat_editable_fields:
                game_stat = self.game_stats[player.id]
                season_stat = self.consolidated_stats[player.id]

                if not games_played_is_updated:
                    player_play_in_the_game = game_stat.player_stats.seconds_played > 0

                    if player_play_in_the_game:
                        season_stat.player_stats.games_played += 1
                        updated_player_stats.append(season_stat.player_stats)

                    games_played_is_updated = True

                game_stat_field_value = getattr(game_stat, field)
                season_stat_field_value = getattr(season_stat, field)

                new_value = game_stat_field_value + season_stat_field_value
                setattr(season_stat, field, new_value)

            updated_season_stats.append(self.consolidated_stats[player.id])

        Stat.stats.bulk_update(
            updated_season_stats,
            self.stat_editable_fields
        )
        PlayerStat.player_stats.bulk_update(
            updated_player_stats,
            ['games_played']
        )


class TeamSeasonStatComputation:
    def __init__(self, game):
        self.game = game

    def compute_both_teams(self):
        self.compute(self.game.home_team)
        self.compute(self.game.away_team)

    def compute(self, team):
        self._set_game_stat(team)
        self._set_consolidated_stat(team)
        self._set_editable_fields()
        self._perform_computations()

    def _set_game_stat(self, team):
        self.game_stat = Stat.stats.filter(
            team_game_stat__team=team,
            team_game_stat__game=self.game
        ).first()

    def _set_consolidated_stat(self, team):
        if self.game.is_eliminations:
            self.consolidated_stat = Stat.stats.filter(
                team_season_stat__team=team,
                team_season_stat__season=self.game.season
            ).first()
        elif self.game.is_playoffs:
            self.consolidated_stat = Stat.stats.filter(
                team_playoffs_stat__team=team,
                team_playoffs_stat__season=self.game.season
            ).first()
        else: # do nothing
            pass

    def _set_editable_fields(self):
        self.stat_editable_fields = get_editable_fields(
            instance=self.game_stat
        )

    def _perform_computations(self):
        for field in self.stat_editable_fields:
            game_stat_field_value = getattr(self.game_stat, field)
            season_stat_field_value = getattr(self.consolidated_stat, field)

            new_value = game_stat_field_value + season_stat_field_value

            setattr(self.consolidated_stat, field, new_value)

        self.consolidated_stat.save()

    
class PlayoffStats:
    def __init__(self, game) -> None:
        self.game = game
    
    def set_playoffs_stats(self):
        home_team_season = self._get_season_team(self.game.home_team)
        away_team_season = self._get_season_team(self.game.away_team)
        self._create_team(self.game.home_team, home_team_season)
        self._create_team(self.game.away_team, away_team_season)

    def _create_team(self, team , team_season):
        if team_season.has_playoffs_stats:
            return
        
        stat = Stat.stats.create(
            stats_type='TP'  # Team Playoffs
        )
        TeamStat.team_stats.create(
            stat=stat
        )
        TeamPlayoffsStat.stats.create(
            season=self.game.season,
            team=team,
            stat=stat
        )

        self._create_players(team)

        team_season.has_playoffs_stats = True
        team_season.save()

    def _get_season_team(self, team):
        return SeasonTeam.teams.filter(
            season=self.game.season,
            team=team
        ).first()
    
    def _create_players(self, team):
        players = team.players.filter(
            season=self.game.season
        )

        for player in players:
            stat = Stat.stats.create(
                stats_type='P'  # Player
            )
            PlayerStat.player_stats.create(
                stats=stat
            )
            PlayerPlayoffsStat.stats.create(
                season=self.game.season,
                player_team=player,
                stat=stat
            )





def get_editable_fields(
    *,
    instance: object
):
    # noinspection PyProtectedMember
    return [
        field.name
        for field in instance._meta.fields
        if field.editable and field.name != 'id' and field.name != 'stats_type'
    ]


def update_game_is_approved_by_admin(
        *,
        game: object,
        user: object
):
    game.is_approved_by_admin = True
    game.approved_by_admin = user
    game.save()


def get_stat_based_on_game_type(
    *,
    game: object,
    team: object
):
    if game.is_eliminations:
        return Stat.stats.filter(
            team_season_stat__season=game.season,
            team_season_stat__team=team
        ).first().team_stats
    elif game.is_playoffs:
        return Stat.stats.filter(
            team_playoffs_stat__season=game.season,
            team_playoffs_stat__team=team
        ).first().team_stats
    else: # do nothing
        pass


def update_teams_win_or_lose(
    *,
    game: object
):
    home_stat = get_stat_based_on_game_type(
        game=game,
        team=game.home_team
    )
    away_stat = get_stat_based_on_game_type(
        game=game,
        team=game.away_team
    )

    is_tie = game.winner is None

    if is_tie:
        return

    the_winner_is_home_team = game.winner == game.home_team

    if the_winner_is_home_team:
        home_stat.win += 1
        away_stat.lose += 1
    else:
        away_stat.win += 1
        home_stat.lose += 1

    home_stat.save()
    away_stat.save()