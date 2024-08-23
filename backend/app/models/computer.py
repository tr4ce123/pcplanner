from django.db import models


class Component(models.Model):
    type = models.CharField(null=True)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pcpp_url = models.URLField(max_length=200, null=True, blank=True)
    specs = models.JSONField(null = True)
    image_url = models.URLField(null=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.name} - ${self.price}"

class FailedURL(models.Model):
    url = models.URLField(max_length=200)

    def __str__(self):
        return f"Failed URL: {self.url}"

class Computer(models.Model):
    name = models.CharField(max_length=255)
    cpu = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="cpu_computers", null=True
    )
    cpu_cooler = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="cpu_cooler_computers", null=True
    )
    gpu = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="gpu_computers", null=True
    )
    motherboard = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="motherboard_computers", null=True
    )
    ram = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="ram_computers", null=True
    )
    psu = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="psu_computers", null=True
    )
    storage = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="storage_computers", null=True
    )
    case = models.ForeignKey(
        Component, on_delete=models.CASCADE, related_name="case_computers", null=True
    )
    total_price = models.FloatField(null=True, blank=True)
    aiResponse = models.CharField(null=True, blank=True)

    # Custome save method that calculates the total price before the model is actually saved into the database
    def save(self, *args, **kwargs):
        # Helper function to ensure price is a float
        def to_float(price):
            try:
                return float(price)
            except (TypeError, ValueError):
                return 0.0

        self.total_price = round(sum(
            [
                to_float(self.cpu.price) if self.cpu else 0,
                to_float(self.cpu_cooler.price) if self.cpu_cooler else 0,
                to_float(self.gpu.price) if self.gpu else 0,
                to_float(self.motherboard.price) if self.motherboard else 0,
                to_float(self.ram.price) if self.ram else 0,
                to_float(self.psu.price) if self.psu else 0,
                to_float(self.storage.price) if self.storage else 0,
                to_float(self.case.price) if self.case else 0,
            ]
        ), 2)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Computer with total price ${self.total_price:.2f}"
