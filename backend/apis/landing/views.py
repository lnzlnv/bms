from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)

from apps.landing.models import (
    MainImage,
    Highlights,
    News
)

from .serializers import (
    MainImageSerializer,
    HighlightSerializer,
    NewsSerializer
)


class MainImageAPIVIew(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = MainImageSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    def get_queryset(self):
        return MainImage.images.all()


class HighlightsAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = HighlightSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return Highlights.videos.all()
    

class NewsAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
):
    serializer_class = NewsSerializer

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)
    
    def get_queryset(self):
        return News.images.all()
    

class PublicHighlightsAPIView(
    GenericAPIView,
    ListModelMixin
):
    paginator = None
    authentication_classes = []
    permission_classes = []
    serializer_class = HighlightSerializer

    def get(self, request, *args, **kwargs):    
        return super().list(request, *args, **kwargs)
    
    def get_queryset(self):
        return Highlights.videos.all()[:5]