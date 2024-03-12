from django.db import models
from management.models import SampleForm
from account.role_choices import ROLE_CHOICES
from management.status import sample_form_form_available
# Create your models here.

class SampleTrack(models.Model):
    sample_form = models.ForeignKey(SampleForm,on_delete = models.CASCADE,related_name = "track_sample")
    form_available = models.PositiveSmallIntegerField(choices=ROLE_CHOICES)
    # track_type
    remarks = models.CharField(max_length = 3000)
    status = models.CharField(choices = sample_form_form_available , max_length = 20)
    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)