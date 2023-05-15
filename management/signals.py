# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm

@receiver(pre_save, sender=SampleFormHasParameter)
def NavigationPreSave(sender, instance, **kwargs):
    SampleFormObj = SampleForm.objects.get(id=instance.sample_form_id)
    SampleFormObj.form_available = instance.form_available
    SampleFormObj.status = instance.status
    SampleFormObj.save()
    
    