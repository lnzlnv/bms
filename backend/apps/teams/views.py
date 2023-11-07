from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class TeamsPageView(TemplateView):
    template_name = 'teams/public-all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_public_all = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get_context_data(self, **kwargs):
        return {'self': self}


class CreateTeamView(LoginRequiredMixin, TemplateView):
    template_name = 'teams/create.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class AllTeamsView(LoginRequiredMixin, TemplateView):
    template_name = 'teams/all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin_teams = 'active'
        self.is_all_teams = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}
