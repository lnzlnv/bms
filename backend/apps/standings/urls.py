from django.urls import path

from . import views

app_name = 'standings'

urlpatterns = [
    path('standings/seniors/',
         views.StandingsPageView.as_view(),
         name='all'),
]
