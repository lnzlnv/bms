from django.urls import path

from . import views


app_name = 'api-teams'

urlpatterns = [
    path('teams/create/options/', 
            views.CreateTeamOptionsAPIVIew.as_view(),
                name='create-options'),
    path('teams/',
            views.TeamsAPIView.as_view(),
                name='create'),
    path('teams/<int:season>/<str:division>/all/',
            views.TeamsAPIView.as_view(),
                name='all'),
    path('teams/<int:pk>/',
            views.TeamsAPIView.as_view(),
                name='team'),
    path('teams/view/public/all/',
            views.TeamsPublicAPIView.as_view(),
                name='public-all'),
    path('teams/import/<int:season>/',
         views.ImportTeamsAPIView.as_view(),
         name='import-team')
]
