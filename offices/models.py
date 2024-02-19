from django.db import models

# Create your models here.

class Branches(models.Model):
    name = models.CharField(max_length=255)
    