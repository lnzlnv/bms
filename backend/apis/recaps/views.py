from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response

from .selectors import get_game_schedules_dates
from .serializers import GameScheduleDateSerializer


class RecapsAPIView(
    GenericAPIView,
    ListModelMixin
):
    serializer_class = GameScheduleDateSerializer
    paginator = None
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        last_5_games = get_game_schedules_dates()[0:5]
        return last_5_games
