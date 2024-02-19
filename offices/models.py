from django.db import models

# Create your models here.

class Branches(models.Model):
    name = models.CharField(max_length=255)

class InspectorType(models.Model):
    name = models.CharField(choices=(('food','Food'),('feed','Feed')), default=None, max_length=155,null=True)

    