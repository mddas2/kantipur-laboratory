from django.db import models
from account.models import CustomUser

# Create your models here.

class Notification(models.Model):
    notification_name = models.CharField(max_length=200,null=True)
    from_notification = models.EmailField(max_length=200,null=True)
    to_notification = models.ManyToManyField(CustomUser,related_name="notification",on_delete= models.CASCADE)
    is_read = models.BooleanField(default=False)

    
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SUPERADMIN'),
        ('SMU','SMU'),
        ('SUPERVISOR', 'SUPERVISOR'),
        ('ANALYST', 'ANALYST'),
        ('USER', 'USER'),
    )
    group_notification = models.CharField(choices=ROLE_CHOICES, blank=True, null=True)
