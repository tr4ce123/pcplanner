from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpenAIView

chatgpt_router = DefaultRouter()
chatgpt_router.register(r"chatgpt", OpenAIView, basename="chatgpt")

# urlpatterns = [
#     path("", include(chatgpt_router.urls)),
#     path('openai/', OpenAIView.as_view(), name='openai'),

# ]
