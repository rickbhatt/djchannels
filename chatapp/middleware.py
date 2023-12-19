from pprint import pprint

import jwt
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.conf import settings
from django.contrib.auth.models import AnonymousUser

from account.models import CustomUser

from .exceptions import JWTAuthMiddlewareError


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        secret_key = settings.SECRET_KEY

        # print("middle ware working")

        if "refresh_token" in scope["cookies"]:
            refresh_token = scope["cookies"].get("refresh_token")
            try:
                decoded_refresh_token = jwt.decode(
                    refresh_token, secret_key, algorithms=["HS256"]
                )

                user_obj = await get_user_by_id(decoded_refresh_token["user_id"])

                scope["user"] = user_obj

            except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
                scope["user"] = AnonymousUser()

            except Exception as e:
                raise JWTAuthMiddlewareError(e)

        else:
            scope["user"] = AnonymousUser()

        return None


@database_sync_to_async
def get_user_by_id(user_id):
    try:
        user_obj = CustomUser.objects.get(id=user_id)

        return user_obj
    except CustomUser.DoesNotExist:
        return AnonymousUser()
