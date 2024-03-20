from django.db import models
from management.models import SampleForm
from account.role_choices import ROLE_CHOICES
from management.status import sample_form_form_available
from websocket import notification_type
from account.models import CustomUser
from .back_track_status import sample_form_back_track_status_choices
# Create your models here.

class SampleTrack(models.Model):
    sample_form = models.ForeignKey(SampleForm,on_delete = models.CASCADE,related_name = "track_sample")
    user = models.ForeignKey(CustomUser,related_name = "track_sample",on_delete = models.SET_NULL,null = True)#from_back
    remarks = models.CharField(max_length = 4000)
    
    status = models.CharField(max_length = 30,choices = sample_form_back_track_status_choices)
    form_available = models.CharField(choices = sample_form_form_available , max_length = 20)   

    to_back = models.ForeignKey(CustomUser,related_name = "take_backs",on_delete = models.CASCADE,null = True)

    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)