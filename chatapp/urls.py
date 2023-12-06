from django.urls import path

from . import views

urlpatterns = [
    path("get-chats/<str:group_name>/", views.get_chats, name="get-chat"),
]
