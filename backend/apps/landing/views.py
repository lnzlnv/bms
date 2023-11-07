from typing import Any
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.public_pages.models import Season
from apps.admin.services import redirect_user_without_permission
from apis.generate_account.selectors import get_activation_requests


class LandingContentDetailsView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/content.html'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.is_admin_landing = 'active'
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {'self': self}
    

class AddImageView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/add-image.html'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {'self': self}
    

class HighlightsView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/highlights.html'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {'self': self}
    

class AddNewsView(LoginRequiredMixin, TemplateView):
    template_name = 'landing/add-news.html'

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self.season = Season.seasons.all().first()
        self.unupdated_accounts = get_activation_requests().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_admin_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        return {'self': self}