from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season
from apis.generate_account.selectors import get_activation_requests


class AnnouncementsCreateView(LoginRequiredMixin, TemplateView):
    template_name = 'announcements/create.html'

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


class AllAnnouncementsView(LoginRequiredMixin, TemplateView):
    template_name = 'announcements/all.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_admin_announcements = 'active'
        self.is_all_announcements = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}
