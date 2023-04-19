from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15 , null=True)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255)  
    image = models.ImageField(upload_to='user/profile', null=True)

    SUPERADMIN = 1
    SMU = 2
    SUPERVISOR = 3
    ANALYST = 4

    ROLE_CHOICES = (
        (SUPERADMIN, 'SUPERADMIN'),
        (SMU,'SMU'),
        (SUPERVISOR, 'SUPERVISOR'),
        (ANALYST, 'ANALYST'),
    )
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def getRoleName(self):
        if self.role==1:
            return 'SUPERADMIN'
        elif self.role==2:
            return 'SMU'
        elif self.role==3:
            return 'SUPERVISOR'
        elif self.role==3:
            return 'ANALYST'
        else:
            return 'None'