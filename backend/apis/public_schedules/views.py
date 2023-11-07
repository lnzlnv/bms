from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin

from apis.game_schedule.serializers import GameScheduleModelSerializer

from .selectors import get_future_games


class PublicSchedulesAPIView(
    GenericAPIView,
    ListModelMixin
):
    authentication_classes = []
    permission_classes = []
    serializer_class = GameScheduleModelSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return get_future_games()
