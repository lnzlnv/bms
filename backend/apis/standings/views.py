from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin
)
from rest_framework.pagination import LimitOffsetPagination


from .serializers import (
    PlayerStatSerializer,
    TeamStatSerializer
)
from .selectors import (
    get_player_standings,
    get_team_standings,
    get_stats
)


class TeamStandingsAPIView(
    GenericAPIView,
    ListModelMixin
):
    paginator = None
    authentication_classes = []
    permission_classes = []
    serializer_class = TeamStatSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.standing_type = request.GET.get('standing_type', None)
        return super().list(request, *args, **kwargs)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['standing_type'] = self.standing_type
        return context

    def get_queryset(self):
        return get_team_standings(
            season=self.kwargs['season'],
            standing_type=self.standing_type
        )


class PlayerStandingsAPIView(
    GenericAPIView,
    ListModelMixin
):
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 20
    serializer_class = PlayerStatSerializer
    authentication_classes = []
    permission_classes = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None
        self.standing_type = None

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        self.standing_type = request.GET.get('standing_type', None)
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return get_player_standings(
            season=self.kwargs['season'],
            division=self.kwargs['division'],
            standing_type=self.standing_type
        )
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['standing_type'] = self.standing_type
        return context


class SinglePlayerStats(
    GenericAPIView,
    RetrieveModelMixin
):
    serializer_class = PlayerStatSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None
        self.standing_type = None
        self.season = None

    def get(self, request, *args, **kwargs):
        self.season = request.GET.get('season', 0)
        self.standing_type = request.GET.get('standing_type', None)
        self.kwargs = kwargs
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        return get_stats(
            season=self.season,
            standing_type=self.standing_type,
            player=self.kwargs['pk']
        )
