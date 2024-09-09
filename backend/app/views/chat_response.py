from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from ..serializers.chat_response import ChatResponseSerializer
from ..serializers.computer import ComputerSerializer
from ..serializers.preferences import PreferencesSerializer
from ..models.chat_response import ChatResponse
from ..models.computer import Component, Computer
from ..models.preferences import Preferences
from dotenv import load_dotenv
import re, requests, os, logging
from pypartpicker import Scraper

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_KEY"])

class ChatResponseViewSet(ModelViewSet):
    queryset = ChatResponse.objects.all()
    serializer_class = ChatResponseSerializer

    def create(self, request):
        computer_id = request.data.get('computer_id')
        user_prompt = request.data.get('userPrompt')
        computer = None

        try:
            computer = Computer.objects.get(id=computer_id)
        except Computer.DoesNotExist:
            return Response({"error": "Computer not found."}, status=status.HTTP_404_NOT_FOUND)
        
        if not user_prompt:
            return Response({"error": "User prompt is missing."}, status=status.HTTP_400_BAD_REQUEST)
        
        components = [
            f"{computer.cpu.name} (Specs: {computer.cpu.specs})" if computer.cpu else "CPU missing",
            f"{computer.cpu_cooler.name} (Specs: {computer.cpu_cooler.specs})" if computer.cpu_cooler else "CPU cooler missing",
            f"{computer.gpu.name} (Specs: {computer.gpu.specs})" if computer.gpu else "GPU missing",
            f"{computer.motherboard.name} (Specs: {computer.motherboard.specs})" if computer.motherboard else "Motherboard missing",
            f"{computer.ram.name} (Specs: {computer.ram.specs})" if computer.ram else "RAM missing",
            f"{computer.psu.name} (Specs: {computer.psu.specs})" if computer.psu else "PSU missing",
            f"{computer.storage.name} (Specs: {computer.storage.specs})" if computer.storage else "Storage missing",
            f"{computer.case.name} (Specs: {computer.case.specs})" if computer.case else "Case missing"
        ]

        component_details = ", ".join(components)
        detailed_prompt = f"""Given a computer with {component_details}, and price {computer.total_price}. 
        Provide a structured, concise response under 200 words to this user's question. 
        If the user asks for different parts or reconstructed budget include the new total price at the bottom. 
        If not, don't add it. User prompt: {user_prompt}."""


        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": detailed_prompt}],
            )

            # Grab the response
            generated_text = response.choices[0].message.content.strip()

            chat_response = ChatResponse.objects.create(
                prompt=detailed_prompt,
                response=generated_text,
            )

            computer.aiResponse = generated_text
            computer.save()

            response_data = {
                "chat_response": ChatResponseSerializer(chat_response).data
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)