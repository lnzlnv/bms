from apps.statisticians.models import PlayerTeam

def normalize_query(
    *,
    query: []
):
    data = {}

    for item in query:
        data[item.id] = item
    return data


def get_current_season_players_ids(
    *,
    team: object,
    season: object or int
):
    players = PlayerTeam.players.filter(
        team=team,
        season=season
    )

    return [player.player.id for player in players]