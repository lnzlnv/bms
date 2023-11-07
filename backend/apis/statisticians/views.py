from django.http import Http404
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response

from apps.game_schedule.models import Game
from apps.statisticians.models import (
    Stat,
)
from apps.statisticians.services import get_game

from .serializers import (
    GameScheduleSerializer,
    GamesTodayOptions,
    GameSerializer,
    StatsSerializer,
    SubstitutionSerializer,
    QuarterSerializer
)
from .services import (
    get_todays_games_schedules,
    update_game_quarter,
    set_game_starters,
    update_team_points_classification,
    set_winner,
    TeamGameStats,
    PlayerGameStats,
    ValidatedData,
    SubstitutionTime,
    PointsPerQuarter,
    TeamStatsAnalysis,
    delete_officiate_history
)


class GamesTodayOptionsAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(GamesTodayOptions(request.user).data)


class GamesAPIView(
    GenericAPIView,
    ListModelMixin
):
    serializer_class = GameScheduleSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        return get_todays_games_schedules()


class OfficiateGameAPIView(
    GenericAPIView,
    RetrieveModelMixin,
    UpdateModelMixin,
):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None
        self.is_get = None

    def dispatch(self, request, *args, **kwargs):
        self.is_get = request.method == 'GET'
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        game = self.get_object()

        if not game.player_stats_are_generated:
            PlayerGameStats(game=game).create()
            TeamGameStats(game=game).create()

        return super().retrieve(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        serializer = SubstitutionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        if self.is_get:
            return Game.games.all()
        return Stat.stats.all()
    
    def get_serializer_class(self):
        if self.is_get:
            return GameSerializer
        return StatsSerializer
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['statistician'] = self.request.user
        return context
    
    def perform_update(self, serializer):
        ValidatedData(
            game_id=self.kwargs['game'],
            team_id=self.kwargs['team'],
            data=self.request.data,
            validated_data=serializer.validated_data,
            stats=self.get_object()
        ).update()

        serializer.save()
    
    def perform_create(self, serializer):
        SubstitutionTime(
            data=serializer.validated_data,
            game=get_game(game=self.kwargs['game']),
            team_id=self.kwargs['team']
        ).record()


class GameQuarterAPIView(
    GenericAPIView
):
    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = QuarterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def perform_update(self, serializer):
        game = get_game(game=self.kwargs['game'])
        
        if game is None:
            raise Http404()

        quarter = serializer.validated_data['quarter']

        update_team_points_classification(
            game=game,
            team=game.home_team
        )

        PointsPerQuarter(
            game=game,
            quarter=quarter
        ).set()

        update_game_quarter(
            game=game,
            quarter=quarter
        )

        if not game.starters_are_set:
            set_game_starters(game=game)


class GenerateTimeAnalysis(GenericAPIView):
    def post(self, request, *args, **kwargs):
        game = get_game(game=self.kwargs['game'])

        if game.has_half_time_analysis and kwargs['quarter'] == 2:
            return Response(
                {'message': 'Already has half-time analysis. Please delete the current analysis to create another one.'}, 
                status=400
            )
        
        if game.has_full_time_analysis and kwargs['quarter'] >=4:
            return Response(
                {'message': 'Already has full-time analysis. Please delete the current analysis to create another one.'}, 
                status=400
            )
        
        if kwargs['quarter'] != 2 and kwargs['quarter'] < 3:
            return Response(
                {'message': 'Only Half-Time and Full time analysis can be generated'},
                status=400
            )

        TeamStatsAnalysis(
            game=game,
            quarter=kwargs['quarter']
        ).create()

        if kwargs['quarter'] == 2:
            game.has_half_time_analysis = True
        elif kwargs['quarter'] >= 4:
            game.has_full_time_analysis = True
            game.is_finished = True
            set_winner(game=game)
        else:  # do nothing
            pass

        game.save()

        return Response({'message': 'success'})