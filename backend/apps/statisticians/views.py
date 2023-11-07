from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from apps.admin.services import redirect_user_without_permission
from apps.public_pages.models import Season


class GamesTodayView(LoginRequiredMixin, TemplateView):
    template_name = 'statisticians/games_today.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_games = 'active'
        self.is_games_today = 'active'
        self.season = Season.seasons.all().first()

    def get(self, request, *args, **kwargs):
        return redirect_user_without_permission(
            is_allowed=request.user.has_statistician_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        return {'self': self}


class OfficiateGameView(LoginRequiredMixin, TemplateView):
    template_name = 'statisticians/officiate_game.html'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.game_id = None
        self.kwargs = None
        self.is_games = 'active'
        self.is_officiate_game = 'active'
        self.season = Season.seasons.all().first()

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return redirect_user_without_permission(
            is_allowed=request.user.has_statistician_privileges,
            default=super().get(request, *args, **kwargs)
        )

    def get_context_data(self, **kwargs):
        self.game_id = self.kwargs['game'].split('-')[-1]
        return {'self': self}
