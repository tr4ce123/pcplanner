from rest_framework.viewsets import ModelViewSet
from ..serializers.computer import ComponentSerializer, ComputerSerializer
from ..models.computer import Component, Computer


class ComponentViewSet(ModelViewSet):
    queryset = Component.objects.all()
    serializer_class = ComponentSerializer


class ComputerViewSet(ModelViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
