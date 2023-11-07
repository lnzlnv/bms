from typing import Any, Dict

from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import (
    HttpResponseRedirect
)
from django.urls import (
    reverse,
    reverse_lazy
)
from django.views.generic import (
    RedirectView
)

from apps.public_pages.models import Season

from .models import User


class LoginPageView(LoginView):
    template_name = 'authentication/login.html'
    success_url = reverse_lazy('authentication:redirect-based-on-role')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_login = 'active'
        self.form = None
        self.season = Season.seasons.all().first()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(
                reverse('authentication:redirect-based-on-role')
            )
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        self.form = self.get_form()
        return {'self': self}


class RedirectBasedOnUserRoleView(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args: Any, **kwargs: Any):
        user = self.request.user

        if not user.is_updated:
            return reverse('user_profile:update', args=(user.username,))

        if user.is_super_administration:
            return reverse('games_for_admin_approval:all')
        
        if user.is_statistician:
            return reverse('statisticians:games-today')
        
        if user.is_super_statistician:
            return reverse('super_statistician:stats-approval')
        
        if user.is_administration:
            return reverse('game_schedule:all')


class AccountActivationRequest(FormView):
    template_name = 'authentication/activation-request.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.has_request_activation = False
        self.season = Season.seasons.all().first()

    def post(self, request, *args, **kwargs):
        self.user = User.objects.filter(username=kwargs['username']).first()
        self.user.has_activation_request = True
        self.user.save()
        self.has_request_activation = True
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        return {'self': self}
