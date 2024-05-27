from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatGPTResponseViewSet

chatgpt_router = DefaultRouter()
chatgpt_router.register(r"chatgpt", ChatGPTResponseViewSet)
