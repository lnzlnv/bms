from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.mixins import (
    CreateModelMixin, 
    ListModelMixin,
    UpdateModelMixin,
    DestroyModelMixin
)
from rest_framework.response import Response

from apps.game_schedule.models import (
    Game,
    GameSchedule,
    Season
)
from apps.teams.models import Team
from apps.public_pages.models import ScheduleBanner

from .serializers import (
    CurrentSeasonSerializer,
    GameScheduleSerializer,
    GameScheduleModelSerializer,
    GameScheduleOptionsSerializer, 
    GameScheduleEditSerializer,
    ScheduleBannerSerializer,
    ScheduleBannerOptionSerializer,
    ScheduleBannerModelSerializer
)
from .services import (
    create_game,
    create_game_schedule,
    update_game_schedule,
    update_game,
    get_schedule_banners,
    get_season
)


class GameScheduleAPIView(
        GenericAPIView, 
        CreateModelMixin, 
    ):

    def get(self, request, *args, **kwargs):
        self.season = request.GET.get('season')
        serializer = GameScheduleOptionsSerializer(
            instance=request.user, 
            **self.get_context_data()
        )
        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = GameScheduleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._create_schedule(serializer.data)
        return Response(serializer.data)
    
    def get_context_data(self, **kwargs):
        context = {
            'season': self.season
        }
        return context
    
    def _create_schedule(self, data):
        game_schedule = create_game_schedule(
            data=data,
            user=self.request.user
        )

        game = create_game(
            data=data,
            schedule=game_schedule
        )


class AllScheduleAPIView(
    GenericAPIView,
    ListModelMixin,
    CreateModelMixin,
):
    serializer_class = GameScheduleModelSerializer

    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().list(request, *args, **kwargs)

    def get_queryset(self):
        return GameSchedule.schedules.filter(
            season=self.kwargs['season'],
            division=self.kwargs['division']
        ).order_by('-date')


class DeleteSingleSchedule(GenericAPIView):
    def post(self, request, *args, **kwargs):
        schedule = get_object_or_404(GameSchedule, pk=kwargs['pk'])
        schedule.delete()
        return Response({'message': 'success'})


class SeasonsAPIView(
    GenericAPIView, 
):
    def get(self, request, *args, **kwargs):
        serializer = CurrentSeasonSerializer(request.user)
        return Response(serializer.data)


class EditScheduleAPIView(
    GenericAPIView,
    UpdateModelMixin,
):
    def post(self, request, *args, **kwargs):
        self.kwargs = kwargs
        serializer = GameScheduleEditSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._update_schedule(serializer.data)
        return Response(serializer.data)
    
    def _update_schedule(self, data):
        gameSchedule = get_object_or_404(GameSchedule, pk=self.kwargs['pk'])
        
        if gameSchedule is None:
            return
        
        season = get_season(season=data['season'])
        update_game_schedule(
            data=data,
            schedule=gameSchedule,
            season=season
        )

        update_game(
            data=data,
            game=gameSchedule.game,
            season=season
        )


class ScheduleBannerAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    def dispatch(self, request, *args, **kwargs):
        self.is_delete = self.request.method == 'DELETE'
        self.is_update = self.request.method == 'PUT'
        
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().list(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        if self.is_delete or self.is_update:
            return ScheduleBanner.schedules.all()

        return get_schedule_banners(
            season=self.kwargs['season'],
            division=self.kwargs['division']
        )
    
    def get_serializer_class(self):
        if self.is_delete or self.is_update:
            return ScheduleBannerModelSerializer
        
        return ScheduleBannerSerializer
    
    def perform_create(self, serializer):
        serializer.save(
            creator=self.request.user
        )


class CreateScheduleBannerOptionsAPIView(
    GenericAPIView
):
    def get(self, request, *args, **kwargs):
        serializer = ScheduleBannerOptionSerializer(request.user)
        return Response(serializer.data)