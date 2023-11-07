from typing import Any, Dict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


from .services import redirect_user_without_permission


class AccessNotGrantedView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/access_not_granted.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return {'self': self}


class CreateSeasonView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/new_season.html'

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


class AllSeasonView(LoginRequiredMixin, TemplateView):
    template_name = 'admin/all_season.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin_season = 'active'
        self.is_all_season = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}
