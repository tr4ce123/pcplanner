from rest_framework.serializers import ModelSerializer
from ..models.chat_response import ChatResponse
from ..serializers.preferences import PreferencesSerializer


class ChatResponseSerializer(ModelSerializer):
    preference = PreferencesSerializer(read_only=True)

    class Meta:
        model = ChatResponse
        fields = "__all__"
