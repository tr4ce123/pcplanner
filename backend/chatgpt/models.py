from django.db import models


class ChatGPTResponse(models.Model):
    prompt = models.TextField(default="default prompt")
    response = models.TextField(default="default response")

    def __str__(self):
        return f"Response: {self.response[:50]}..."
