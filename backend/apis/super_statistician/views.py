from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from apis.statisticians.services import (
    TeamStatsAnalysis
)
from apis.statisticians.serializers import (
    GameScheduleSerializer,
    PointsClassificationSerializer,
)
from apps.statisticians.services import get_game
from apps.statisticians.models import (
    Stat,
    PointsClassification,
    PointsInAQuarter
)
from apps.game_schedule.models import Game, GameSchedule

from .serializers import (
    GameStatsApprovalSerializer,
    GameSerializer,
    PointsInAQuarterSerializer
)
from .serializers_2 import StatsSerializer
from .selectors import get_unapproved_games_stats
from .services import (
    approved_stats,
    update_minutes_played,
    update_team_stats,
    get_field_value
)


class GameStatsApprovalOptions(GenericAPIView):
    def get(self, request, *args, **kwargs):
        serializer = GameStatsApprovalSerializer(request.user)
        return Response(serializer.data)


class GamesStatsForApprovalAPIView(
    GenericAPIView,
    ListModelMixin,
    DestroyModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin
):
    def dispatch(self, request, *args, **kwargs):
        self.is_retrieve = 'pk' in kwargs

        hasType = 'type' in kwargs
        self.is_update_classification = hasType and \
            kwargs['type'] == 'classification'
        self.is_update_stat = not hasType
        self.is_update_quarter_points = hasType and \
            kwargs['type'] == 'quarter'

        self.is_get_list = request.method == 'GET' and not self.is_retrieve
        self.is_delete = request.method == 'DELETE'
        self.is_patch = request.method == 'PATCH'

        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args ,**kwargs):
        if 'pk' in self.kwargs:
            return super().retrieve(request, *args, **kwargs)

        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        game = get_object_or_404(Game, pk=kwargs['pk'])

        if game.is_approved_by_super_statistician:
            return Response({'message': 'Already approved.'})
        
        approved_stats(
            game=game,
            user=self.request.user
        )

        return Response({'message': 'approved'})
    
    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'success'})
    
    def get_serializer_class(self):
        if self.is_get_list:
            return GameScheduleSerializer
        
        if self.is_patch and self.is_update_stat:
            return StatsSerializer
        
        if self.is_patch and self.is_update_classification:
            return PointsClassificationSerializer
        
        if self.is_patch and self.is_update_quarter_points:
            return PointsInAQuarterSerializer
        
        return GameSerializer
    
    def perform_update(self, serializer):
        if self.is_update_stat:
            data = serializer.validated_data
            if 'minutes' in data:
                update_minutes_played(
                    instance=self.get_object(),
                    minutes=data['minutes']
                )

            player_stat_is_updated = self.kwargs['team_stat'] > 0

            if player_stat_is_updated:
                value = get_field_value(
                    instance=self.get_object(),
                    data=data
                )

                update_team_stats(
                    data=data,
                    field_old_value=value,
                    stat=self.kwargs['team_stat']
                )

        return super().perform_update(serializer)

    def get_queryset(self):
        if self.is_get_list:
            return get_unapproved_games_stats()

        if self.is_delete:
            return GameSchedule.schedules.all()
        
        if self.is_patch and self.is_update_stat:
            return Stat.stats.all()
        
        if self.is_patch and self.is_update_classification:
            return PointsClassification.classifications.all()

        if self.is_patch and self.is_update_quarter_points:
            return PointsInAQuarter.quarter_points.all()
        
        return Game.games.all()


class GenerateFullTimeAnalysisAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        game = get_game(game=kwargs['game'])

        if game.has_full_time_analysis:
            return Response({'message': 'Analysis has been generated'})

        data = { 
            'quarter': game.quarter,
            'minutes': 0,
            'seconds': 0 
        }

        TeamStatsAnalysis(
            game=game,
            validated_data=data
        ).create()
        
        game.has_full_time_analysis = True
        game.save()

        return Response({'message': 'success'})