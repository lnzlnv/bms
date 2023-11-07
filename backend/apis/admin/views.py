from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
)
from rest_framework.response import Response

from apps.authentication.models import User
from apps.public_pages.models import Season

from .serializers import (
    UserRequestSerializer,
    SeasonSerializer
)
from .services import create_teams_season_stat


class UserRequestAPIView(
        GenericAPIView, 
        ListModelMixin, 
        UpdateModelMixin
    ):
    serializer_class = UserRequestSerializer
    queryset = User.objects.filter(status='P')

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)
    
    def perform_update(self, serializer):
        # super().perform_update(serializer)
        user = self.get_object()

        if user.is_super_administration:
            serializer.save(is_superuser=True)
        
        serializer.save()


class SeasonAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = SeasonSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'success'})
    
    def get_queryset(self):
        return Season.seasons.all().order_by('-year')

    def perform_create(self, serializer):
        create_teams_season_stat(season=serializer.save())