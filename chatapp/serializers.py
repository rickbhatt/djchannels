from rest_framework import serializers
from .models import Chat


class AllChatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = "__all__"
