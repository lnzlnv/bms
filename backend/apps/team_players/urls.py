from django.urls import path, include

from . import views

app_name = 'team_players'

urlpatterns = [
    path('<str:division>/<str:team>/players/', include([
        path('',
             views.TeamPlayersView.as_view(),
             name='all'),
        path('create/',
             views.CreatePlayerView.as_view(),
             name='create'),
    ])),
]
