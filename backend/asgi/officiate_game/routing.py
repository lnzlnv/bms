from django.urls import path

from . import consumers


urlpatterns = [
    path("<str:game_slug>/", 
                consumers.StatsUpdateConsumer.as_asgi()),
]