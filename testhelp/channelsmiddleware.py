from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from jwt import decode as jwt_decode
from testhelp import settings

User = get_user_model()


@database_sync_to_async
def get_user(validated_token):
    try:
        user = User.objects.get(id=validated_token["user_id"])
        print(f"{user}")
        return user

    except User.DoesNotExist:
        return AnonymousUser()


class JwtAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        close_old_connections()

        # check if the token exists in the query parameters
        headers = dict(scope["headers"])
        authorization = headers.get(b"authorization")

        if authorization:
            token_type, _, token = authorization.decode().partition(" ")
            if token_type.lower() == "bearer":
                try:
                    decoded_data = jwt_decode(
                        token, settings.SECRET_KEY, algorithms=["HS256"]
                    )
                    scope["user"] = await get_user(validated_token=decoded_data)
                except Exception as e:
                    print(e)

        return await super().__call__(scope, receive, send)


def JwtAuthMiddlewareStack(inner):
    return JwtAuthMiddleware(AuthMiddlewareStack(inner))
