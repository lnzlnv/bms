from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests

from .services import get_team


class TeamPlayersView(LoginRequiredMixin, TemplateView):
    template_name = 'team_players/all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team = None
        self.kwargs = None
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        self.team = get_team(
            slug=self.kwargs['team'],
            division=self.kwargs['division'][0]
        )
        return {'self': self}


class CreatePlayerView(LoginRequiredMixin, TemplateView):
    template_name = 'team_players/create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.team = None
        self.kwargs = None
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        self.team = get_team(
            slug=self.kwargs['team'],
            division=self.kwargs['division'][0]
        )
        return {'self': self}
