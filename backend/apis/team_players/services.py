from rest_framework import serializers

from apps.teams.models import (
    PlayerTeam,
    Player,
)
from apps.public_pages.models import Season
from apps.statisticians.models import (
    PlayerSeasonStat,
    PlayerStat,
    Stat,
)
from apis.game_schedule.services import (
    get_team,
    get_season
)

def get_player_team(
    *,
    number: int,
    team: int,
    season: int
):
    return PlayerTeam.players.filter(
        number=number,
        season__year=season,
        team=team
    ).first()


def get_player_team_2(
    *,
    pk: int
):
    return PlayerTeam.players.filter(pk=pk).first()


def create_player(
    *,
    data: dict
):
    return Player.players.create(
        height_feet=data['height_feet'],
        height_inches=data['height_inches'],
        weight=data['weight'],
        first_name=data['first_name'],
        last_name=data['last_name']
    )



def create_player_team(
    *,
    data: {},
    team: int,
    player: Player
):
    team = get_team(team=team)

    season = get_season(season=data['season'])

    return PlayerTeam.players.create(
        player=player,
        team=team,
        season=season,
        position=data['position'],
        number=data['player_number']
    )


def create_player_season_stat(
    *,
    player: PlayerTeam,
    season_year: int
):
    stats_type = 'PS'  # Player Season Type
    stat = Stat.stats.create(
        stats_type=stats_type
    )
    PlayerStat.player_stats.create(
        stats=stat
    )

    season = get_season(season=season_year)
    PlayerSeasonStat.stats.create(
        season=season,
        player_team=player,
        stat=stat
    )


def get_season_2(
    *,
    season_id: int
):
    return Season.seasons.filter(pk=season_id).first()


def get_previous_season():
    seasons = Season.seasons.all()[:2]
    if seasons.count() <= 1:
        return None
    return seasons[1]


def edit_player(
    *,
    player_team,
    data
):
    player_team.season = get_season_2(season_id=data['season'])

    player_team.number = data['player_number']
    player_team.position = data['position']

    player = player_team.player

    player.height_feet = data['height_feet']
    player.height_inches = data['height_inches']
    player.weight = data['weight']
    player.first_name = data['first_name']
    player.last_name = data['last_name']

    player_team.save()
    player.save()
