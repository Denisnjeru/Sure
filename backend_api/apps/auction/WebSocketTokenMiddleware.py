from urllib.parse import parse_qs

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import close_old_connections
from channels.auth import AuthMiddleware, AuthMiddlewareStack, UserLazyObject
from channels.db import database_sync_to_async
from channels.sessions import CookieMiddleware, SessionMiddleware
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()

"""[Denis]
plucks the JWT access token from the query string and retrieves the associated user.
  Once the WebSocket connection is opened, all messages can be sent and received without
  verifying the user again. Closing the connection and opening it again 
  requires re-authorization.
"""


@database_sync_to_async
def get_user(scope):
    close_old_connections()
    token = scope['cookies']['token']
    if not token:
        return AnonymousUser()
    try:
        access_token = AccessToken(token)
        user = User.objects.get(id=access_token['user_id'])
    except Exception as exception:
        return AnonymousUser()
    if not user.is_active:
        return AnonymousUser()
    return user


class TokenAuthMiddleware(AuthMiddleware):
    async def resolve_scope(self, scope):
        scope['user']._wrapped = await get_user(scope)


def TokenAuthMiddlewareStack(inner):
    return CookieMiddleware(SessionMiddleware(TokenAuthMiddleware(inner)))
