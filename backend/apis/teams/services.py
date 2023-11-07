from apps.teams.models import (
    Team,
    SeasonTeam
)
from apps.statisticians.models import (
    Stat,
    TeamSeasonStat,
    TeamStat
)
from apps.public_pages.models import Season


def create_team_season_stat(
    team: Team,
    season: int or object
):
    stat_type = 'T'  # Team
    stat = Stat.stats.create(
        stats_type=stat_type
    )
    TeamStat.team_stats.create(stat=stat)
    TeamSeasonStat.stats.create(
        season=season,
        team=team,
        stat=stat
    )


def create_season_team(
    team: Team,
    season: int
):
    SeasonTeam.teams.create(
        season=season,
        team=team
    )


def get_teams(
    *,
    season: int,
    division: str
):
    return Team.teams.filter(
        participated_season__season=season,
        division=division
    )


def get_teams_not_in_season(
    season: int
):
    return Team.teams.exclude(participated_season__season=season)


def import_teams(
    *,
    teams: list,
    season: int
):
    teams = Team.teams.filter(pk__in=teams)
    season = Season.seasons.filter(pk=season).first()
    seasonTeams = []
    stats = [] 
    team_stats = [] 
    team_season_stats = []

    for team in teams:
        seasonTeams.append(SeasonTeam(
            season=season,
            team=team
        ))
        stat_type = 'T'  # Team
        stat = Stat(stats_type=stat_type)
        team_stat = TeamStat(stat=stat)
        team_season_stat = TeamSeasonStat(
            season=season,
            team=team,
            stat=stat
        )

        stats.append(stat)
        team_stats.append(team_stat)
        team_season_stats.append(team_season_stat)

    SeasonTeam.teams.bulk_create(seasonTeams)
    Stat.stats.bulk_create(stats)
    TeamStat.team_stats.bulk_create(team_stats)
    TeamSeasonStat.stats.bulk_create(team_season_stats)