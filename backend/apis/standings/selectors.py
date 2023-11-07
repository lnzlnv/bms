from apps.statisticians.models import (
    PlayerStat,
    TeamStat,
)


def get_player_standings(
    *,
    division: str,
    season: object or int,
    standing_type: str
):
    if standing_type == 'ELIMINATIONS' or standing_type is None:
        return PlayerStat.player_stats.filter(
            stats__player_season_stat__season=season,
            stats__player_season_stat__player_team__team__division=division
        )

    if standing_type == 'PLAYOFFS':
        return PlayerStat.player_stats.filter(
            stats__player_playoffs_stat__season=season,
            stats__player_playoffs_stat__player_team__team__division=division
        )


def get_team_standings(
    *,
    season: int or object,
    standing_type: str
):
    if standing_type == 'ELIMINATIONS' or standing_type is None:
        return TeamStat.team_stats.filter(
                stat__team_season_stat__season=season
            ).order_by('-win', 'lose')

    if standing_type == 'PLAYOFFS':
        return TeamStat.team_stats.filter(
                stat__team_playoffs_stat__season=season
            ).order_by('-win', 'lose')


def get_stats(
    *,
    season: int or object,
    player: int or object,
    standing_type: str
):
    if standing_type == 'ELIMINATIONS' or standing_type is None:
        return PlayerStat.player_stats.filter(
            stats__player_season_stat__season=season,
            stats__player_season_stat__player_team=player
        ).first()

    if standing_type == 'PLAYOFFS':
        return PlayerStat.player_stats.filter(
            stats__player_playoffs_stat__season=season,
            stats__player_playoffs_stat__player_team=player
        ).first()
