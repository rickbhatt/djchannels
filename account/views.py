from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status, exceptions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser
from .utils import calc_token_exp
from django.conf import settings

from .permissions import IsUnauthenticated


@api_view(["POST"])
@permission_classes([IsUnauthenticated])
def handle_login(request):
    email = request.data.get("email")
    password = request.data.get("password")

    try:
        user = CustomUser.objects.get(email=email)

        if not user.is_active:
            raise exceptions.AuthenticationFailed("The account is inactive")

        authenticated_user = authenticate(email=user.email, password=password)

        if authenticated_user is None:
            raise exceptions.AuthenticationFailed("Credentials did not match")

        refresh = RefreshToken.for_user(authenticated_user)

        refresh_token = str(refresh)

        refresh_token_exp = calc_token_exp(refresh_token)

        access_token = str(refresh.access_token)

        access_token_exp = calc_token_exp(access_token)

        user_data = {
            "is_active": user.is_active,
            "is_superuser": user.is_superuser,
            "is_staff": user.is_staff,
            "user_name": user.user_name,
        }

        response = Response({"user": user_data}, status=status.HTTP_200_OK)

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=True,
            samesite="Strict",
            path="/",
            expires=access_token_exp,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=False,
            secure=True,
            samesite="Strict",
            path="/",
            expires=refresh_token_exp,
        )

        return response

    except CustomUser.DoesNotExist:
        raise exceptions.AuthenticationFailed("Account does not exist")

    except exceptions.AuthenticationFailed as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@permission_classes([AllowAny])
def handle_token_refresh(request):
    try:
        token = request.data.get("refresh")

        refresh = RefreshToken(token)

        refresh_token = str(refresh)
        access_token = str(refresh.access_token)

        access_token_exp = calc_token_exp(access_token)
        refresh_token_exp = calc_token_exp(refresh_token)

        response = Response(
            {"message": "refreshed access token"}, status=status.HTTP_200_OK
        )

        # Set new access token in the cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=False,
            secure=True,
            samesite="Strict",
            path="/",
            expires=access_token_exp,
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=False,
            secure=True,
            samesite="Strict",
            path="/",
            expires=refresh_token_exp,
        )

        return response

    except exceptions.RefreshError as e:
        return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
