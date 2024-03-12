from django.db import models
from management.models import SampleForm
from account.role_choices import ROLE_CHOICES
from management.status import sample_form_form_available
from websocket import notification_type
from account.models import CustomUser
# Create your models here.

class SampleTrack(models.Model):
    sample_form = models.ForeignKey(SampleForm,on_delete = models.CASCADE,related_name = "track_sample")
    form_available = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    user = models.ForeignKey(CustomUser,related_name = "track_sample",on_delete = models.SET_NULL,null = True)
    track_types = models.CharField(max_length = 33, choices = notification_type.notification_type )
    remarks = models.CharField(max_length = 2000)
    form_available_string = models.CharField(choices = sample_form_form_available , max_length = 20)    
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)