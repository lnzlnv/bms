from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season


class GameStatsApprovalView(LoginRequiredMixin, TemplateView):
    template_name = 'super_statistician/game_stats_approval.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_game_stats_approvals = 'active'
        self.season = Season.seasons.all().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_statistician,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class GameStatsReports(LoginRequiredMixin, TemplateView):
    template_name = 'super_statistician/reports.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game = None
        self.kwargs = None
        self.is_game_stats_approvals = 'active'
        self.is_reports = 'active'
        self.season = Season.seasons.all().first()

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_statistician,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        self.game = self.kwargs['game_slug'].split('-')[-1]
        return {'self': self}
