from django.urls import path
from . import views

urlpatterns = [
    path("send-admin-message/<str:group_name>/", views.send_message_from_admin)
]
