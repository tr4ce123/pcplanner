from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.preferences import PreferencesViewSet
from .views.computer import ComponentViewSet, ComputerViewSet, FailedURLViewSet
from .views.chat_response import ChatResponseViewSet

router = DefaultRouter()
router.register(r"preferences", PreferencesViewSet)
router.register(r"components", ComponentViewSet, basename="components")
router.register(r"failedurls", FailedURLViewSet, basename="failedurls")
router.register(r"computers", ComputerViewSet, basename="computers")
router.register(r"chatresponses", ChatResponseViewSet, basename="chatresponses")

urlpatterns = [path("", include(router.urls))]
