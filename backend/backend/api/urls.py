from rest_framework.routers import DefaultRouter
from pcplanner.api.urls import preferences_router
from django.urls import path, include

router = DefaultRouter()

router.registry.extend(preferences_router.registry)

urlpatterns = [path("", include(router.urls))]
