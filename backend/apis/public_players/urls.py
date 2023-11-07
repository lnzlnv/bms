from django.urls import path

from . import views


app_name = 'api_players_public'


urlpatterns = [
	path('options/',
			views.PlayersPublicOptionsAPIView.as_view(),
				name='options'),
	path('<int:season>/<int:team>/',
			views.PlayersPublicAPIView.as_view(),
				name='players')
]