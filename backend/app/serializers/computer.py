from rest_framework.serializers import ModelSerializer, SerializerMethodField
from ..models.computer import Component, Computer


class ComponentSerializer(ModelSerializer):
    class Meta:
        model = Component
        fields = "__all__"


class ComputerSerializer(ModelSerializer):
    components = SerializerMethodField()

    class Meta:
        model = Computer
        fields = [
            "id",
            "components",
            "total_price",
        ]

    def get_components(self, obj):
        return {
            "cpu": ComponentSerializer(obj.cpu).data,
            "cpuCooler": ComponentSerializer(obj.cpu_cooler).data,
            "gpu": ComponentSerializer(obj.gpu).data,
            "motherboard": ComponentSerializer(obj.motherboard).data,
            "ram": ComponentSerializer(obj.ram).data,
            "psu": ComponentSerializer(obj.psu).data,
            "storage": ComponentSerializer(obj.storage).data,
            "case": ComponentSerializer(obj.case).data,
        }
