from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import ChatGPTResponse
from .serializers import ChatGPTResponseSerializer
from pcplanner.models import Preferences
import openai

openai.api_key = "your_openai_api_key"


class ChatGPTResponseViewSet(viewsets.ModelViewSet):
    queryset = ChatGPTResponse.objects.all()
    serializer_class = ChatGPTResponseSerializer

    @action(detail=False, methods=["post"])
    def get_pc_parts(self, request):
        preference_id = request.data.get("preference_id")

        try:
            preference = Preferences.objects.get(id=preference_id)
        except Preferences.DoesNotExist:
            return Response(
                {"error": "Preferences not found for the given ID"},
                status=status.HTTP_404_NOT_FOUND,
            )

        prompt = f"Given a budget of ${preference.budget}, recommend the highest performing computer parts without exceeding the budget but getting as close as you can."

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response.choices[0].message["content"]
            chatgpt_response = ChatGPTResponse.objects.create(response=result)
            return Response(
                ChatGPTResponseSerializer(chatgpt_response).data,
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
