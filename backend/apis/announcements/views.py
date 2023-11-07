from datetime import datetime


from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)

from apps.announcements.models import Announcement

from .serializers import AnnouncementSerializer


class AnnouncementsAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = AnnouncementSerializer

    def dispatch(self, request, *args, **kwargs):
        self.is_update = request.method == 'PUT'
        self.is_get_list = request.method == 'GET'
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'success'})
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def get_queryset(self):
        if self.is_get_list:
            return Announcement.announcements.all()
        
        return Announcement.announcements.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['is_update'] = self.is_update
        return context