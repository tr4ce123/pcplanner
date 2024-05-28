import json
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from .serializers import ChatGPTResponseSerializer
from ..models import ChatGPTResponse
from pcplanner.models import Preferences
import os
from dotenv import load_dotenv


load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_KEY"])


class OpenAIView(ModelViewSet):
    queryset = ChatGPTResponse.objects.all()
    serializer_class = ChatGPTResponseSerializer

    def create(self, request):
        try:
            preferences_id = request.data.get("preferenceId")

            if not preferences_id:
                return Response(
                    {"error": "Preferences ID is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            preferences = Preferences.objects.get(id=preferences_id)
            prompt = f"""What are the highest performing computer parts I can buy with a budget of ${preferences.budget}? Give a list of the parts in a numbered list: 1. CPU 2. CPU Cooler 3. GPU 4. Motherboard 5. RAM 6. PSU 7. SSD 8. Case. 
            All of the parts must be compatable with each other. Keep within plus or minus $50 of the given budget."""

            # Generates the response from GPT 3.5 Turbo model
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )

            # Parse the response
            generated_text = response.choices[0].message.content.strip()

            # Load response into model
            chatgpt_response = ChatGPTResponse.objects.create(
                prompt=prompt, response=generated_text
            )

            serializer = self.get_serializer(chatgpt_response)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
