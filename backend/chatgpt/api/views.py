from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from openai import OpenAI
from .serializers import (
    ChatGPTResponseSerializer,
    ComputerSerializer,
)
from ..models import ChatGPTResponse, Component, Computer
from pcplanner.models import Preferences
import os
from dotenv import load_dotenv
import re, requests
from pypartpicker import Scraper

load_dotenv()
client = OpenAI(api_key=os.environ["OPENAI_KEY"])
scraperAPI = os.environ["SCRAPER_API_KEY"]


def scraperapi_response_retriever(url, **kwargs):
    scraperapi_url = f"http://api.scraperapi.com/?api_key={scraperAPI}&url={url}"
    response = requests.get(scraperapi_url, **kwargs)
    response.raise_for_status()
    return response


pcpp = Scraper(response_retriever=scraperapi_response_retriever)


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
            All of the parts must be compatable with each other. Keep within plus or minus $50 of the given budget. Format it in this way: 1. CPU: Product Name - Price 2. CPU Cooler: Product Name - Price 3. GPU: Product Name - Price 4. Motherboard: Product Name - Price 5. RAM: Product Name - Price 6. PSU: Product Name - Price 7. SSD: Product Name - Price 8. Case: Product Name - Price Total Cost: Price. For example: 1. CPU: AMD Ryzen 5 3600 - $199.99.
            Use parts that are the most recent as possible unless the budget is lower. Try not to suggest things that have been released before 2020. Don't give a brand, just give the component but adding AMD or Intel or Nvidia is okay just not different sellers. Try to keep it to just the model of the part if possible."""

            # Generates the response from GPT 3.5 Turbo model
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
            )

            # Grab the response
            generated_text = response.choices[0].message.content.strip()

            # Regular expression that parses the string and extracts each component based on ChatGPT's structured response
            pattern = r"\d+\. ([^:]+): ([^$]+) - \$(\d+\.\d+)"
            matches = re.findall(pattern, generated_text)

            # Dictionary / Hashmap to store component objects
            components = {}

            for match in matches:
                component = Component.objects.create(
                    name=match[1].strip(), price=match[2]
                )
                components[match[0].strip().replace(" ", "_").lower()] = component

            # Find total price and store it
            total_price_match = re.search(r"Total Cost: \$(\d+\.\d+)", generated_text)
            total_price = (
                float(total_price_match.group(1)) if total_price_match else None
            )

            for component_key, component_instance in components.items():
                print(
                    f"Searching for component: {component_instance.name}"
                )  # Debug statement
                parts = pcpp.part_search(component_instance.name, limit=1)
                if parts:
                    product = pcpp.fetch_product(parts[0].url)
                    if product.price:
                        try:
                            component_instance.price = float(
                                product.price.replace("$", "").replace(",", "")
                            )
                            component_instance.save()
                            print(
                                f"Updated {component_key} price to {component_instance.price}"
                            )  # Debug statement
                        except Exception as e:
                            print(
                                f"Error updating price for {component_key}: {e}"
                            )  # Debug statement
                    else:
                        print(f"No price found for {component_key}")  # Debug statement
                else:
                    print(f"No parts found for {component_key}")  # Debug statement

            # Load components into Computer model
            computer = Computer.objects.create(
                cpu=components.get("cpu"),
                cpu_cooler=components.get("cpu_cooler"),
                gpu=components.get("gpu"),
                motherboard=components.get("motherboard"),
                ram=components.get("ram"),
                psu=components.get("psu"),
                storage=components.get("ssd"),
                case=components.get("case"),
                total_price=total_price,
            )

            # Load response into model
            chatgpt_response = ChatGPTResponse.objects.create(
                prompt=prompt, response=generated_text
            )

            response_data = {
                "chatgpt_response": ChatGPTResponseSerializer(chatgpt_response).data,
                "computer": ComputerSerializer(computer).data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ComputerViewSet(ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
