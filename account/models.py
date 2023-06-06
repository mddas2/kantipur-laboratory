from django.db import models
# from management.models import ClientCategory

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15 , null=True)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255,unique=True)  

    renew_document = models.ImageField(upload_to='media/user/renew_doument', null=True)
    registration_document = models.ImageField(upload_to='media/user/registration', null=True)
    department_name = models.CharField(max_length=255,null=True) 
    department_address = models.CharField(max_length=255,null=True) 
    registration_number = models.CharField(max_length=255,null=True) 

    is_active = models.BooleanField(default=True)

    is_verified = models.IntegerField(choices=[(0, 'Not verified'), (1, 'Verified')], default=0)
    client_category = models.ForeignKey("management.ClientCategory",related_name="user",on_delete=models.CASCADE,null=True)    

    SUPERADMIN = 1
    SMU = 2
    SUPERVISOR = 3
    ANALYST = 4
    USER = 5
    VERIFIER = 6

    ROLE_CHOICES = (
        (SUPERADMIN, 'SUPERADMIN'),
        (SMU,'SMU'),
        (SUPERVISOR, 'SUPERVISOR'),
        (ANALYST, 'ANALYST'),
        (USER, 'USER'),
        (VERIFIER, 'VERIFIER'),
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
        
    def save(self, *args, **kwargs):
        self.is_active = True  # Ensure is_active is always True
        super().save(*args, **kwargs)