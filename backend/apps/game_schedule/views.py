from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class CreateScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'game_schedule/create_schedule.html'

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


class AllScheduleView(LoginRequiredMixin, TemplateView):
    template_name = 'game_schedule/all_schedule.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_all_schedule = 'active'
        self.is_admin_schedule = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class CreateScheduleBannerView(LoginRequiredMixin, TemplateView):
    template_name = 'game_schedule/banner.html'

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


class AllScheduleBannerView(LoginRequiredMixin, TemplateView):
    template_name = 'game_schedule/banner_all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin_banner = 'active'
        self.is_banner_all = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}
