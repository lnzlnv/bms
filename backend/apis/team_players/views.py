from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    RetrieveModelMixin,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response

from apps.teams.models import (
    PlayerTeam,
)
from apps.teams.models import Team
from .selectors import (
    get_current_season_players_ids
)
from .serializers import (
    TeamPlayersOptionsSerializer,
    PlayerCreateSerializer,
    PlayerTeamSerializer
)
from .services import (
    create_player,
    create_player_team,
    create_player_season_stat,
    get_player_team_2,
    edit_player,
    get_previous_season,
)

from .services_classes import Players


class TeamPlayersOptions(
    GenericAPIView,
    RetrieveModelMixin
):
    serializer_class = TeamPlayersOptionsSerializer
    queryset = Team.teams.all()

    def get(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


class TeamPlayerAPIVIew(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
):
    paginator = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.player_team = None
        self.kwargs = None
        self.is_previous_players = None
        self.is_update = None
        self.is_create = None

    def dispatch(self, request, *args, **kwargs):
        self.is_create = request.method == 'POST'
        self.is_update = request.method == 'PUT'
        self.is_previous_players = 'type' in kwargs and kwargs['type'] == 'previous'
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'success'})
    
    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_serializer_class(self):
        if self.is_create:
            return PlayerCreateSerializer
        
        return PlayerTeamSerializer

    def get_queryset(self):
        return PlayerTeam.players.filter(
            team=self.kwargs['pk'],
            season=self.kwargs['season']
        )
    
    def get_object(self):
        return PlayerTeam.players.filter(pk=self.kwargs['pk']).first()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['team'] = self.kwargs['pk'] if not self.is_update else self.kwargs['team']
        context['is_update'] = self.is_update

        if self.is_update:
            self.player_team = get_player_team_2(pk=self.kwargs['pk'])
            context['player'] = self.player_team
        
        return context

    def update(self, request, *args, **kwargs):
        serializer = PlayerCreateSerializer(
            data=request.data,
            context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def perform_create(self, serializer):
        data = serializer.validated_data
        
        player = create_player(data=data)
        player.save()
        
        player_team = create_player_team(
            data=data,
            player=player,
            team=self.kwargs['pk']
        )
        create_player_season_stat(
            player=player_team,
            season_year=data['season']
        )
        
        player_team.save()

    def perform_update(self, serializer):
        edit_player(
            player_team=self.player_team,
            data=serializer.validated_data
        )


class ImportPlayersAPIView(
    GenericAPIView,
    ListModelMixin
):
    serializer_class = PlayerTeamSerializer
    paginator = None

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        players = Players(kwargs, request.data)

        players.validate_data()

        if players.has_errors:
            return Response(players.errors, status=403)

        players.perform_create()

        return Response({'message': 'success'})

    def get_queryset(self):
        current_season_players = get_current_season_players_ids(
            team=self.kwargs['team'],
            season=self.kwargs['season']
        )
        return PlayerTeam.players.filter(
            team=self.kwargs['team'],
            season=get_previous_season()
        ).exclude(player__in=current_season_players)
