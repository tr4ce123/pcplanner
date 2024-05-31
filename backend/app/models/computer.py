from django.db import models


class Component(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - ${self.price}"


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
    total_price = models.FloatField()

    # Custome save method that calculates the total price before the model is actually saved into the database
    def save(self, *args, **kwargs):
        # Helper function to ensure price is a float
        def to_float(price):
            try:
                return float(price)
            except (TypeError, ValueError):
                return 0.0

        self.total_price = sum(
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
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Computer with total price ${self.total_price:.2f}"
