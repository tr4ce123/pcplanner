import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from ..serializers.computer import ComponentSerializer, ComputerSerializer, FailedURLSerializer
from ..serializers.preferences import PreferencesSerializer
from ..models.computer import Component, Computer, FailedURL
from ..models.preferences import Preferences
from ..services.pcpp import ScraperService
from ..services.computer import ComputerService


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer

    @action(detail=False, methods=['post'])
    def load_database(self, request):
        try:
            scraper = ScraperService()
            scraper.load_cases()
            return Response({"status": "Database loaded successfully."}, status=status.HTTP_200_OK)
        except requests.exceptions.RequestException as e:
            # Handle exceptions related to HTTP requests
            return Response({"error": f"HTTP Request failed: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            # Handle any other exceptions
            return Response({"error": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class FailedURLViewSet(ModelViewSet):
    queryset = FailedURL.objects.all()
    serializer_class = FailedURLSerializer


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

        computer_service = ComputerService()
        try:
            computer = computer_service.create_computer(preferences)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        computer_serializer = ComputerSerializer(computer)
        return Response(computer_serializer.data, status=status.HTTP_201_CREATED)
