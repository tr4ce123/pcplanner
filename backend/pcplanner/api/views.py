from rest_framework.viewsets import ModelViewSet
from ..models import Preferences
from .serliazers import PreferencesSerializer


class PreferencesViewSet(ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
