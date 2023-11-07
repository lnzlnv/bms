from apps.game_schedule.models import GameSchedule


def get_game_schedules_dates():
    """Get the dates of the games that are already finished
    @return list of game schedules which game results are already approved by the admin
    """
    dates = GameSchedule.schedules.filter(
        game__approved_by_admin=True
    ).raw(
        "SELECT MAX(id) as id, date_formatted "
        "FROM ( "
        "SELECT "
        "schedule.id, "
        "TO_CHAR(schedule.date, 'Dy Mon DD') AS date_formatted, "
        "game.schedule_id "
        "FROM game_schedule_gameschedule as schedule, game_schedule_game as game "
        "WHERE game.schedule_id = schedule.id AND "
        "game.is_approved_by_admin = 't' "
        ") AS subquery "
        "GROUP BY date_formatted "
        "ORDER BY TO_DATE(date_formatted, 'DY, Mon DD') DESC"
    )
    return list(dates)
