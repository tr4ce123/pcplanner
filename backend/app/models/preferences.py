from django.db import models


class Preferences(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    chipset = models.CharField(max_length=50)

    def __str__(self):
        return f"Preferences ID: {self.id}, Budget: {self.budget}"
