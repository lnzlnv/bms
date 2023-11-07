from channels.sessions import CookieMiddleware, SessionMiddleware
from channels.auth import AuthMiddleware, get_user
from channels.db import database_sync_to_async
from django.db import close_old_connections

class CustomAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope)

        if not scope['user'].is_authenticated:
            raise ValueError('UnAuthenticated')


def AuthMiddleWareStack(inner):
    return CookieMiddleware(SessionMiddleware(CustomAuthMiddleware(inner)))