from rest_framework import serializers
from ..models import ChatGPTResponse


class ChatGPTResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPTResponse
        fields = ["id", "prompt", "response"]
