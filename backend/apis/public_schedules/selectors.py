from  datetime import datetime

from apps.game_schedule.models import GameSchedule


def get_future_games():
    now = datetime.now()
    return GameSchedule.schedules.filter(
        date__date__gte=now
    )
