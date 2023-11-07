from apps.game_schedule.models import Game


def get_games_stats_reports(
    *,
    is_approved: bool,
    season: int or object,
    division: str
):
    if not is_approved:
        return Game.games.filter(
            is_approved_by_super_statistician=True,
            is_approved_by_admin=is_approved
        )
    
    return Game.games.filter(
        is_approved_by_super_statistician=True,
        is_approved_by_admin=is_approved,
        season=season,
        home_team__division=division
    )
