from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class GenerateAccount(LoginRequiredMixin, TemplateView):
    template_name = 'generate_account/generate.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_generate_account = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_administration,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class UnupdatedAccountsView(LoginRequiredMixin, TemplateView):
    template_name = 'generate_account/unupdated.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_unupdated_accounts = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.is_super_administration,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}
