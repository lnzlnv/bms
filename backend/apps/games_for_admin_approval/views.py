from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class GamesForApprovalView(LoginRequiredMixin, TemplateView):
    template_name = 'games_for_admin_approval/all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_games_for_approval = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_administration,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class GameStatsReportsView(LoginRequiredMixin, TemplateView):
    template_name = 'games_for_admin_approval/reports.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_id = None
        self.is_games_for_approval = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_administration,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        self.game_id = self.kwargs['game'].split('-')[-1]
        return {'self': self}
