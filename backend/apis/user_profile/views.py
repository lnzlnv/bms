from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password


from apps.authentication.models import User

from .serializers import UserSerializer


class UpdateProfileAPIView(
    GenericAPIView,
    UpdateModelMixin
):
    serializer_class = UserSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_post = None

    def dispatch(self, request, *args, **kwargs):
        self.is_post = request.method == 'POST'
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['password'] = make_password(
            request.data['password1'],
            hasher='pbkdf2_sha256'
        )
        super().partial_update(request, *args, **kwargs)
        return Response({'message': 'success'})

    def perform_update(self, serializer):
        serializer.save(
            is_updated=True
        )

    def get_queryset(self):
        return User.objects.all()
