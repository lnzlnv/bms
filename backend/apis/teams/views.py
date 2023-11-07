from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)

from apps.teams.models import (
    Team,
    SeasonTeam
)
from apps.public_pages.models import Season

from .serializers import (
    CreateOptionsSerializer,
    TeamSerializer,
    ImportPlayerSerializer
)
from .services import (
    create_team_season_stat,
    create_season_team,
    get_teams,
    get_teams_not_in_season,
    import_teams
)


class CreateTeamOptionsAPIVIew(GenericAPIView):
    def get(self, request, *args, **kwargs):
        serializer = CreateOptionsSerializer(request.user)
        return Response(serializer.data)


class TeamsAPIView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = TeamSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.season = None
        self.kwargs = None

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        self.season = request.GET.get('season', 0)
        return super().destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_object(self):
        if self.request.method == 'DELETE':
            return SeasonTeam.teams.filter(
                season=self.season,
                team=self.kwargs['pk']
            ).first()
        return super().get_object()

    def get_queryset(self):
        if self.request.method == 'PUT':
            return Team.teams.all()

        return get_teams(
            division=self.kwargs['division'],
            season=self.kwargs['season']
        )

    def perform_create(self, serializer):
        season_year = serializer.validated_data.pop('season', None)
        team = serializer.save()
        season = Season.seasons.filter(year=season_year).first()
        
        create_team_season_stat(
            team=team,
            season=season
        )
        create_season_team(
            team=team,
            season=season
        )
        

    def get_serializer_context(self):
        if self.request.method != 'GET':
            return {}
        context = super().get_serializer_context()
        context['season'] =  self.kwargs['season']
        return context


class TeamsPublicAPIView(
    GenericAPIView, 
    ListModelMixin
):
    serializer_class = TeamSerializer
    paginator = None
    authentication_classes = []
    permission_classes = []

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().list(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        return Team.teams.all()
    

class ImportTeamsAPIView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin
):
    paginator = None

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TeamSerializer
        
        return ImportPlayerSerializer

    def perform_create(self, serializer):
        import_teams(
            teams=serializer.validated_data['teams'],
            season=self.kwargs['season']
        )

    def get_queryset(self):
        return get_teams_not_in_season(season=self.kwargs['season'])