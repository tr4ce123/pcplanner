from django.db import models
from ..models.preferences import Preferences


class ChatResponse(models.Model):
    prompt = models.TextField(default="default prompt")
    response = models.TextField(default="default response")
    preferences = models.OneToOneField(
        Preferences, on_delete=models.CASCADE, related_name="chat_responses"
    )

    def __str__(self):
        return f"Response: {self.response}"
