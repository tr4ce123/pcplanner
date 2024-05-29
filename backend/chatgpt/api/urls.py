from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OpenAIView, ComputerViewSet

chatgpt_router = DefaultRouter()
chatgpt_router.register(r"chatgpt", OpenAIView, basename="chatgpt")
chatgpt_router.register(r"computers", ComputerViewSet, basename="computers")
