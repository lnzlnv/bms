from typing import Any, Dict

from django.views.generic import TemplateView

from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class PlayersPublicView(TemplateView):
    template_name = 'players/all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_players_public = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}
