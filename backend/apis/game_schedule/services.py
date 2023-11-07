from datetime import datetime

from apps.teams.models import Team
from apps.authentication.models import User
from apps.game_schedule.models import (
    Game,
    GameSchedule,
    Season
)
from apps.public_pages.models import ScheduleBanner



def get_season(
    *,
    season: int
):
    return Season.seasons.filter(pk=season).first()


def get_team(
    *,
    team: int
):
    return Team.teams.filter(pk=team).first()


def get_current_season():
    return Season.seasons.all().first()


def create_game(
    *,
    data: dict,
    schedule: object
):
    home_team = get_team(team=data['home_team'])
    away_team = get_team(team=data['away_team'])

    return Game.games.create(
        season=get_season(season=data['season']),
        schedule=schedule,
        home_team=home_team,
        away_team=away_team,
        game_type=data['game_type']
    )


def create_game_schedule(
    *, 
    data: dict, 
    user: User
):
    return GameSchedule.schedules.create(
        creator=user,
        season=get_season(season=data['season']),
        date=data['date'],
        division=data['division'],
        venue=data['venue']
    )


def update_game_schedule(
    *,
    data: dict,
    schedule: GameSchedule,
    season: Season
):
    schedule.season = season
    schedule.date = data['date_local']
    schedule.division = data['division']
    schedule.venue = data['venue']
    schedule.save()


def update_game(
    *,
    data: dict,
    game: Game,
    season: Season
):
    game.season = season
    game.home_team = get_team(team=data['home_team_id'])
    game.away_team = get_team(team=data['away_team_id'])
    game.game_type = data['game_type']
    game.save()


def get_schedule_banners(
    *,
    season: int,
    division: str
):
    return ScheduleBanner.schedules.filter(
        season=season,
        division=division
    )


def get_image_name(
    *,
    image: str
):
    return image.split('/')[-1]


def get_formatted_date(
    *,
    date: str
):
    year = date.year
    month = date.month
    day = date.day
    
    hour = date.hour + 8
    if hour < 0:
        hour += 24
        day -= 1
    
    if hour > 23:
        hour -= 24
        day += 1

    minute = date.minute

    date_format = datetime(year, month, day, hour, minute)
    return date_format

def get_formatted_date_2(
    *,
    date: str
):
    year = date.year
    month = date.month
    day = date.day
    hour = date.hour
    minute = date.minute

    date_format = datetime(year, month, day, hour, minute)
    return date_format