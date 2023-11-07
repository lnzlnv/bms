from django.urls import path

from . import views

app_name = 'teams'

urlpatterns = [
    path('teams/seniors/', 
            views.TeamsPageView.as_view(), 
                name='public-all'),
    path('teams/create/',
            views.CreateTeamView.as_view(),
                name='create'),
    path('teams/all/',
            views.AllTeamsView.as_view(),
                name='all')
]