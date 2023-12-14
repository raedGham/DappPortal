from django.db import models

# Create your models here.

class Position (models.Model):
    pos_name = models.CharField(max_length=100,  unique=True, blank=True)
    description = models.TextField(blank=True)

    def __str__(self) :
        return self.pos_name