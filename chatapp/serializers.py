from rest_framework import serializers
from .models import Chat


class AllChatsSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.user_name")

    class Meta:
        model = Chat
        fields = "__all__"
