from django.urls import re_path, path
from channels.routing import URLRouter
from asgi.officiate_game.routing import urlpatterns as officiate_urls

from .officiate_game.consumers import StatsUpdateConsumer

websocket_urlpatterns = [
    path("ws/officiate-game/", URLRouter(officiate_urls))
]