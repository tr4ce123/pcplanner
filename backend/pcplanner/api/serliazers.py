from rest_framework.serializers import ModelSerializer
from ..models import Preferences


class PreferencesSerializer(ModelSerializer):
    class Meta:
        model = Preferences
        fields = ("id", "budget")
