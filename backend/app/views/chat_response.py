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
        





#     def create(self, request):
#         try:
#             preferences_data = request.data.get("preferences")
#             # components = request.data.get("components")

#             if not isinstance(preferences_data, dict):
#                 return Response(
#                     {"error": "Invalid data. Expected a dictionary for preferences."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             preferences_id = preferences_data.get("id")
#             if preferences_id:
#                 try:
#                     preferences = Preferences.objects.get(id=preferences_id)
#                 except Preferences.DoesNotExist:
#                     return Response(
#                         {"error": "Preferences with the given ID does not exist."},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             else:
#                 preferences_serializer = PreferencesSerializer(data=preferences_data)
#                 if preferences_serializer.is_valid():
#                     preferences = preferences_serializer.save()
#                 else:
#                     return Response(
#                         preferences_serializer.errors,
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )

#             prompt = f"""What are the highest performing computer parts I can buy with a budget of ${preferences.budget}? Give a list of the parts in a numbered list: 1. CPU 2. CPU Cooler 3. GPU 4. Motherboard 5. RAM 6. PSU 7. SSD 8. Case. 
#             All of the parts must be compatable with each other. Keep within plus or minus $50 of the given budget. Format it in this way: 1. CPU: Product Name - Price 2. CPU Cooler: Product Name - Price 3. GPU: Product Name - Price 4. Motherboard: Product Name - Price 5. RAM: Product Name - Price 6. PSU: Product Name - Price 7. SSD: Product Name - Price 8. Case: Product Name - Price Total Cost: Price. For example: 1. CPU: AMD Ryzen 5 3600 - $199.99.
#             Use parts that are the most recent as possible unless the budget is lower. Try not to suggest things that have been released before 2020. Don't give a brand, just give the component but adding AMD or Intel or Nvidia is okay just not different sellers. Try to keep it to just the model of the part if possible."""

#             # Generates the response from GPT 3.5 Turbo model
#             response = client.chat.completions.create(
#                 model="gpt-4o",
#                 messages=[{"role": "user", "content": prompt}],
#             )

#             # Grab the response
#             generated_text = response.choices[0].message.content.strip()

#             # Regular expression that parses the string and extracts each component based on ChatGPT's structured response
#             pattern = r"\d+\. ([^:]+): ([^$]+) - \$(\d+\.\d+)"
#             matches = re.findall(pattern, generated_text)

#             # Dictionary / Hashmap to store component objects
#             components = {}

#             for match in matches:
#                 component = Component.objects.create(
#                     name=match[1].strip(), price=match[2]
#                 )
#                 components[match[0].strip().replace(" ", "_").lower()] = component

#             # def clean_price(price_str):
#             #     return float(re.sub(r"[^\d.]", "", price_str))

#             # for component_key, component_instance in components.items():
#             #     print(
#             #         f"Searching for component: {component_instance.name}"
#             #     )  # Debug statement
#             #     parts = pcpp.part_search(component_instance.name, limit=1)
#             #     if parts:
#             #         product = pcpp.fetch_product(parts[0].url)
#             #         if product.price:
#             #             try:
#             #                 component_instance.price = clean_price(product.price)
#             #                 component_instance.save()
#             #                 print(
#             #                     f"Updated {component_key} price to {component_instance.price}"
#             #                 )  # Debug statement
#             #             except Exception as e:
#             #                 print(
#             #                     f"Error updating price for {component_key}: {e}"
#             #                 )  # Error statement
#             #         else:
#             #             print(f"No price found for {component_key}")  # Debug statement
#             #     else:
#             #         print(f"No parts found for {component_key}")  # Debug statement

#             # # Load components into Computer model
#             # computer_data = {
#             #     "cpu": components.get("cpu"),
#             #     "cpu_cooler": components.get("cpu_cooler"),
#             #     "gpu": components.get("gpu"),
#             #     "motherboard": components.get("motherboard"),
#             #     "ram": components.get("ram"),
#             #     "psu": components.get("psu"),
#             #     "storage": components.get("ssd"),
#             #     "case": components.get("case"),
#             # }

#             # computer = Computer.objects.create(**computer_data)

#             # Load response into model
#             chat_response = ChatResponse.objects.create(
#                 prompt=prompt,
#                 response=generated_text,
#                 preferences=preferences,
#             )

#             response_data = {
#                 "chat_response": ChatResponseSerializer(chat_response).data,
#                 # "computer": ComputerSerializer(computer).data,
#             }

#             return Response(response_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response(
#                 {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
#             )


# class ComputerViewSet(ModelViewSet):
#     queryset = Computer.objects.all()
#     serializer_class = ComputerSerializer
