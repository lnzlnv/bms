from .serializers_2 import StatsSerializer
from apis.statisticians.serializers import PointsClassificationSerializer

from .services import get_points_classification
from .services import get_time_stats_analysis

def get_time_analysis_data(
    *,
    quarter: int,
    game_id: int,
    team: object,
):
    analysis = get_time_stats_analysis(
        game_id=game_id,
        team=team,
        time=quarter
    )

    if analysis is None: 
        return

    classification = get_points_classification(
        game_id=game_id,
        team_id=team.id,
        quarter=quarter,
        is_time_analysis=True
    )

    return {
        'stats': StatsSerializer(analysis.stat).data,
        'points_classification': 
            PointsClassificationSerializer(classification).data
    }