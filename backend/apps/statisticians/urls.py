from django.urls import path

from . import views


app_name = 'statisticians'

urlpatterns = [
    path('games/today/',
            views.GamesTodayView.as_view(),
                name='games-today'),
    path('games/officiate/<slug:game>/',
            views.OfficiateGameView.as_view(),
                name='officiate-game'),
]