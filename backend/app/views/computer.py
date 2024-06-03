from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from ..serializers.computer import ComponentSerializer, ComputerSerializer
from ..serializers.preferences import PreferencesSerializer
from ..models.computer import Component, Computer
from ..models.preferences import Preferences
from ..services.pcpp import ScraperService


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComputerViewSet(ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer

    def create(self, request):
        preferences_id = request.data.get("preferences_id")

        if not preferences_id:
            return Response({"error": "Preferences ID is required"}, status=status.HTTP_400_BAD_REQUEST)


        try:
            preferences = Preferences.objects.get(id=preferences_id)
        except Preferences.DoesNotExist:
            return Response({"error": "Preferences not found"}, status=status.HTTP_404_NOT_FOUND)

        scraper_service = ScraperService()
        computer = scraper_service.test_computer(preferences)

        computer_serializer = ComputerSerializer(computer)
        return Response(computer_serializer.data, status=status.HTTP_201_CREATED)
