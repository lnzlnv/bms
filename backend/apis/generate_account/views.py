from django.contrib.auth.hashers import make_password

from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    UpdateModelMixin
)
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

from apps.authentication.models import User

from .services import (
    generate_username,
    generate_password,
    send_user_credentials_to_email_address,
    ActivationStatus
)
from .serializer import GenerateAccountSerializer
from .selectors import (
    get_unupdated_accounts,
    get_activation_requests
)


class GenerateAccountAPIView(
    GenericAPIView,
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin
):
    serializer_class = GenerateAccountSerializer
    pagination_class = LimitOffsetPagination
    pagination_class.default_limit = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.kwargs = None
        self.username = generate_username()
        self.password_raw = generate_password()
        self.password_enc = make_password(
            self.password_raw,
            hasher='pbkdf2_sha256'
        )

    def dispatch(self, request, *args, **kwargs):
        self.kwargs = kwargs
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request.data['username'] = self.username
        request.data['password'] = self.password_enc
        request.data['password_raw'] = self.password_raw
        return super().create(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        super().destroy(request, *args, **kwargs)
        return Response({'message': 'success'})

    def perform_create(self, serializer):
        super().perform_create(serializer)
        send_user_credentials_to_email_address(
            email=serializer.validated_data['email'],
            username=self.username,
            password=self.password_raw
        )

    def get_queryset(self):
        return get_unupdated_accounts()


class GenerateAccountOptions(GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(User.ROLES)


class SendCredentialsViaEmailAPIView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        user = User.objects.filter(pk=kwargs['pk']).first()
        send_user_credentials_to_email_address(
            email=user.email,
            username=user.username,
            password=user.password_raw
        )
        return Response({'message': 'success'})


class AccountActivationRequestAPIView(
    GenericAPIView,
    ListModelMixin,
    UpdateModelMixin
):
    serializer_class = GenerateAccountSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_approved = None

    def get(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.is_approved = int(request.GET.get('is_approved'))
        return super().partial_update(request, *args, **kwargs)

    def perform_update(self, serializer):
        user = self.get_object()
        serializer.save(has_activation_request=False)
        activation_request = ActivationStatus(
            email=user.email,
            is_approved=self.is_approved,
            site_url=self.request.build_absolute_uri('/')  # Get the main site URL
        )
        activation_request.send_email_status()

    def get_queryset(self):
        return get_activation_requests()
