from typing import List

from .models import Team


def get_all_participating_schools(
) -> List[Team]:
    """get all the participating schools

    Returns:
        list[Team]: list of participating schools
    """
    return Team.teams.raw('SELECT MAX(id) AS id, name FROM teams_team GROUP BY name ORDER BY name')


def get_teams(
    *,
    division: str
) -> List[Team]:
    """get teams based on division

    Args:
        division (str): division name

    Returns:
        list[Team]: teams on the specified division
    """
    return Team.teams.filter(division=division)