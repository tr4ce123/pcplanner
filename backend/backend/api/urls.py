from rest_framework.routers import DefaultRouter
from chatgpt.api.urls import chatgpt_router
from pcplanner.api.urls import preferences_router
from django.urls import path, include

router = DefaultRouter()

router.registry.extend(preferences_router.registry)
router.registry.extend(chatgpt_router.registry)

urlpatterns = [
    path("", include(router.urls)),
]
