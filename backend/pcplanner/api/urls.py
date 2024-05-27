from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import PreferencesViewSet

preferences_router = DefaultRouter()
preferences_router.register(r"preferences", PreferencesViewSet)
