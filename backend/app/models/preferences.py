from django.db import models


class Preferences(models.Model):
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    chipset = models.CharField(max_length=50, null=True, blank=True)
    need_wifi = models.BooleanField(default=True, null=True, blank=True)
    usage = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Preferences ID: {self.id}, Budget: {self.budget}"
