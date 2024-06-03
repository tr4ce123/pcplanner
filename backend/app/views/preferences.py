from rest_framework.viewsets import ModelViewSet
from ..models.preferences import Preferences
from ..serializers.preferences import PreferencesSerializer


class PreferencesViewSet(ModelViewSet):
    queryset = Preferences.objects.all()
    serializer_class = PreferencesSerializer
