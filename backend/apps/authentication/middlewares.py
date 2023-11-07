from django.contrib.auth.middleware import (
    AuthenticationMiddleware as BaseMiddleware,
    get_user
)
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import  logout


class AuthenticationMiddleware(BaseMiddleware):
    def process_request(self, request):
        user = get_user(request)
        if not user.is_anonymous and user.is_expired:
            logout(request)
            return HttpResponseRedirect(
                reverse('authentication:activation-request',
                        args=(user.username,))
            )

        return super().process_request(request)
