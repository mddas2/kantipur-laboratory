# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm,ClientCategory

@receiver(pre_save, sender=SampleFormHasParameter)
def NavigationPreSave(sender, instance, **kwargs):
    SampleFormObj = SampleForm.objects.get(id=instance.sample_form_id)
    SampleFormObj.form_available = instance.form_available
    SampleFormObj.status = instance.status
    SampleFormObj.save()
    
@receiver(pre_save, sender=ClientCategory)
def ClientCategoryPreSave(sender, instance, **kwargs):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    notification_message = "A client Category has created"
    path = "/dashboard/settings"
    

    # Send the notification message to the user's channel
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin',
        {
            'type': 'group.message',
            'message': notification_message
        }
    )