from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .models import Chat
from .serializers import AllChatsSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_chats(request, group_name):
    try:
        print(request.user)

        chat_objs = Chat.objects.filter(group__name=group_name.lower())
        serialized_chats = AllChatsSerializer(chat_objs, many=True).data
        return Response(serialized_chats, status=status.HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
