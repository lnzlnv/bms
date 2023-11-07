from apps.game_schedule.models import Game, GameSchedule
from apps.statisticians.models import (
    PointsInAQuarter
)


def get_unapproved_games_stats():
    return GameSchedule.schedules.filter(
        game__is_approved_by_super_statistician=False,
        game__player_stats_are_generated=True
    )


def get_points_in_a_quarter(
    *,
    game_id: int,
    team_id: int
):
    return PointsInAQuarter.quarter_points.filter(
        game=game_id,
        team=team_id
    )