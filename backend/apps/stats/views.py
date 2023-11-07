from typing import Any, Dict
from django.urls import reverse
from django.views.generic import TemplateView

from apps.teams.models import (
    PlayerTeam,
    Team
)
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests
from apps.statisticians.models import (
    PlayerSeasonStat,
)
from asgi.officiate_game.services import get_id


class PlayerStatsPageView(TemplateView):
    template_name = 'stats/players.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_stats = 'active'
        self.is_player = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class TeamStatsPageView(TemplateView):
    template_name = 'stats/teams.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_stats = 'active'
        self.is_team = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class SinglePlayerStats(TemplateView):
    template_name = 'stats/single_player.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_team_id = None
        self.kwargs = None
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        self.player_team_id = get_id(string=self.kwargs['player'])
        return {'self': self}
