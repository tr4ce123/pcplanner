from rest_framework.decorators import api_view
from rest_framework.response import Response
from pcplanner.models import Preferences
import openai

openai.api_key = "sk-proj-zeT6W3AHpruVx0r91uNFT3BlbkFJ4T666bmzsqyp6aWfnQHr"


@api_view(["POST"])
def get_pc_parts(request):
    budget = request.data.get("budget")

    preference = Preferences.objects.get(budget=budget)

    prompt = f"Given a budget of ${preference.budget}, recommend the highest performing computer parts that are the closest to, but do not exceed the budget. Give a CPU, GPU, RAM kit, Motherboard, Case, Power Supply, and CPU Cooler."

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    result = response.choices[0].message["content"]
    return Response({"result": result}, status=200)
