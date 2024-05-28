from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from .serializers import ChatGPTResponseSerializer
from ..models import ChatGPTResponse
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_KEY"])


class OpenAIView(ModelViewSet):
    queryset = ChatGPTResponse.objects.all()
    serializer_class = ChatGPTResponseSerializer

    def create(self, request, *args, **kwargs):
        prompt = request.data.get("prompt")
        if not prompt:
            return Response(
                {"error": "Prompt is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            generated_text = response.choices[0].message.content.strip()
            chatgpt_response = ChatGPTResponse.objects.create(
                prompt=prompt, response=generated_text
            )
            serializer = self.get_serializer(chatgpt_response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
