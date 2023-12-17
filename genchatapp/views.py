from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from chatapp.models import Chat
from channels.layers import get_channel_layer
import json
from asgiref.sync import async_to_sync


@api_view(["POST"])
@permission_classes([AllowAny])
def send_message_from_admin(request, group_name):
    try:
        message = request.data.get("message")

        username = request.data.get("username")

        channel_layer = get_channel_layer()

        send_data = {"user": "Admin", "message": message}

        if username:
            async_to_sync(channel_layer.group_send)(
                username, {"type": "chat.message", "data": json.dumps(send_data)}
            )
        else:
            async_to_sync(channel_layer.group_send)(
                group_name, {"type": "chat.message", "data": json.dumps(send_data)}
            )

        return Response(
            {"message": "sent message to the group"}, status=status.HTTP_200_OK
        )

    except Exception as e:
        print(f"An exception occurred {e}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
