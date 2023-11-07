from apps.game_schedule.models import Game
from django.http import HttpResponseRedirect
from django.urls import reverse


def get_game(
    *,
    game: int
):
    return Game.games.filter(pk=game).first()


def redirect_user_without_permission(
    *,
    user: object,
    default,  # function
):
    if not user.is_super_statistician and not user.is_statistician:
        return HttpResponseRedirect(
            reverse('administration:access-not-granted')
        )

    return default
