from rest_framework.serializers import ModelSerializer
from ..models.preferences import Preferences


class PreferencesSerializer(ModelSerializer):

    class Meta:
        model = Preferences
        fields = "__all__"
