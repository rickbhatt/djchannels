from channels.middleware import BaseMiddleware
import jwt
from django.conf import settings
from .exceptions import JWTAuthMiddlewareError
from channels.db import database_sync_to_async
from account.models import CustomUser


class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        secret_key = settings.SECRET_KEY

        # print("middle ware working")

        if "access_token" in scope["cookies"]:
            access_token = scope["cookies"]["access_token"]

            refresh_token = scope["cookies"]["refresh_token"]

            try:
                decoded_acccess_token = jwt.decode(
                    access_token, secret_key, algorithms=["HS256"]
                )

                user_obj = await get_user_by_id(decoded_acccess_token["user_id"])

                scope["user"] = user_obj

            except jwt.ExpiredSignatureError:
                pass
            except jwt.InvalidTokenError:
                pass

            except Exception as e:
                raise JWTAuthMiddlewareError(e)

        return await super().__call__(scope, receive, send)


@database_sync_to_async
def get_user_by_id(user_id):
    try:
        user_obj = CustomUser.objects.get(id=user_id)

        return user_obj
    except CustomUser.DoesNotExist:
        return None
