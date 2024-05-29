from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class Computer(models.Model):
    cpu = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="cpu", null=True
    )
    cpu_cooler = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="cpu_cooler", null=True
    )
    gpu = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="gpu", null=True
    )
    motherboard = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="motherboard", null=True
    )
    ram = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="ram", null=True
    )
    psu = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="psu", null=True
    )
    storage = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="storage", null=True
    )
    case = models.OneToOneField(
        Component, on_delete=models.CASCADE, related_name="case", null=True
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)


class ChatGPTResponse(models.Model):
    prompt = models.TextField(default="default prompt")
    response = models.TextField(default="default response")

    def __str__(self):
        return f"Response: {self.response[:50]}..."
