from apps.public_pages.models import Season
from apps.statisticians.models import (
    Stat,
    TeamSeasonStat,
    TeamStat
)
from apps.teams.models import Team


def create_teams_season_stat(
    *,
    season: Season
):
    teams = Team.teams.filter(
        participated_season__season=season
    )
    stats = []
    team_stats = []
    team_season_stats = []

    for team in teams:
        stat_type = 'T'  # Team Type
        stat = Stat(stats_type=stat_type)
        team_stat = TeamStat(stat=stat)
        season_stat = TeamSeasonStat(
            season=season,
            team=team,
            stat=stat
        )

        stats.append(stat)
        team_stats.append(team_stat)
        team_season_stats.append(season_stat)

    Stat.stats.bulk_create(stats)
    TeamStat.team_stats.bulk_create(team_stats)
    TeamSeasonStat.stats.bulk_create(team_season_stats)

