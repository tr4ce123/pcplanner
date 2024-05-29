from rest_framework import serializers
from ..models import ChatGPTResponse, Component, Computer


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        fields = ["name", "price"]


class ComputerSerializer(serializers.ModelSerializer):
    components = serializers.SerializerMethodField()

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


class ChatGPTResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatGPTResponse
        fields = ["id", "prompt", "response"]
