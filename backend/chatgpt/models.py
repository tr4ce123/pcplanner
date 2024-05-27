from django.db import models


class ChatGPTResponse(models.Model):
    budget = models.CharField(max_length=10)
    response = models.TextField()

    def __str__(self):
        return f"Response: {self.response[:50]}..."
