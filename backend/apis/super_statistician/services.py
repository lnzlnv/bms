from apps.statisticians.models import (
    PointsClassification,
    TeamTimeStatsAnalysis,
)
from apps.authentication.models import User
from apps.statisticians.models import Stat


def get_points_classification(
    *,
    game_id: int,
    team_id: int,
    quarter=0,
    is_time_analysis=False
) -> PointsClassification:
    return PointsClassification.classifications.filter(
        game=game_id,
        team=team_id,
        is_time_analysis=is_time_analysis,
        quarter=quarter
    ).first()


def get_time_stats_analysis(
    *,
    game_id: int,
    team: object,
    time: int
):
    return TeamTimeStatsAnalysis.analyses.filter(
        game=game_id,
        team=team,
        time=time
    ).first()


def get_user(
    *,
    user_id: int
):
    return User.objects.filter(pk=user_id).first()


def approved_stats(
    *,
    game: object,
    user: object
):    
    game.is_approved_by_super_statistician = True
    
    game.approved_by_super_statistician = user
    game.save()


def update_minutes_played(
    *,
    instance: object,
    minutes: int
):
    instance.player_stats.seconds_played = minutes * 60
    instance.player_stats.save()


def update_team_stats(
    *,
    data: dict,
    field_old_value: int,
    stat: object or int
):
    if type(stat) is int:
        stat = Stat.stats.filter(pk=stat).first()

    for key in data:
        value_to_be_added = data[key] - field_old_value
        team_stat_value = getattr(stat, key)
        new_team_stat_value = team_stat_value + value_to_be_added
        setattr(stat, key, new_team_stat_value)

    stat.save()


def get_field_value(
    *,
    instance: object,
    data: dict
):
    value = 0
    for key in data:
        value = getattr(instance, key)

    return value
