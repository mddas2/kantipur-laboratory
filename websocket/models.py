from django.db import models
from account.models import CustomUser
from django.utils import timezone

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

# Create your models here.

class Notification(models.Model):
    content_type = models.ForeignKey(ContentType,on_delete=models.CASCADE,null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type','object_id')

    notification_type = models.CharField(max_length=200,null=True,default="push")

    notification_message = models.CharField(max_length=200,null=True)
    particular_message = models.TextField(null=True)
    from_notification = models.ForeignKey(CustomUser,related_name="notifications",on_delete=models.CASCADE,null=True)
    path = models.CharField(max_length=1000,null=True)

    to_notification = models.ManyToManyField(CustomUser,related_name="notification")
    is_read = models.BooleanField(default=False)

    group_notification = models.CharField(max_length = 1000,blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)