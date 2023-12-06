from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path("login/", views.handle_login),
    path("token/refresh/", views.handle_token_refresh, name="token-refresh"),
]
