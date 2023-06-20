from django.db import models
from account.models import CustomUser
from django.utils import timezone

# Create your models here.

class Notification(models.Model):
    notification_message = models.CharField(max_length=200,null=True)
    from_notification = models.CharField(max_length=200,null=True)
    path = models.CharField(max_length=1000,null=True)
    model_name = models.CharField(max_length=200,null=True)
    to_notification = models.ManyToManyField(CustomUser,related_name="notification")
    is_read = models.BooleanField(default=False)
    ROLE_CHOICES = (
        ('SUPERADMIN', 'SUPERADMIN'),
        ('SMU','SMU'),
        ('SUPERVISOR', 'SUPERVISOR'),
        ('ANALYST', 'ANALYST'),
        ('USER', 'USER'),
    )
    group_notification = models.CharField(max_length = 1000,choices=ROLE_CHOICES, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)