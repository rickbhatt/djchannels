import jwt
from datetime import datetime, timezone
from django.utils import timezone as django_timezone
from django.conf import settings


class TokenExpiredError(Exception):
    pass


class InvalidTokenError(Exception):
    pass


def decode_jwt_token(token):
    secret_key = settings.SECRET_KEY

    try:
        decoded_token = jwt.decode(token, secret_key, algorithms=["HS256"])
        return decoded_token
    except jwt.ExpiredSignatureError:
        raise TokenExpiredError("Token has expired.")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token.")


def calc_token_exp(token):
    try:
        decoded_token = decode_jwt_token(token)

        exp_timestamp = decoded_token["exp"]
        # Convert 'exp' timestamp to a datetime object in UTC
        exp_utc = datetime.utcfromtimestamp(exp_timestamp).replace(tzinfo=timezone.utc)

        # Convert UTC datetime to the local time zone
        # exp_local = exp_utc.astimezone(django_timezone.get_current_timezone())

        expiration_time = exp_utc.strftime("%a, %d %b %Y %H:%M:%S GMT")

        return expiration_time
    except Exception as e:
        print(str(e))
