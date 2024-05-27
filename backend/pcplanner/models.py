from django.db import models

# Create your models here.


class Preferences(models.Model):
    budget = models.CharField(max_length=10)

    def __str__(self):
        return f"PC Budget: {self.budget}"
