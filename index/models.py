from django.db import models

# Create your models here.
class Event(models.Model):
    id = models.CharField(max_length=5, primary_key=True, unique=True)
    name = models.CharField(max_length=63, default="")

    def __str__(self):
        return f'{self.id} {self.name}'