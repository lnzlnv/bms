from django.urls import path

from . import views


app_name = 'players'

urlpatterns = [
    path('players/public/all/',
            views.PlayersPublicView.as_view(),
                name='all'),
]