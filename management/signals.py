# signals.py

from django.db.models.signals import pre_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm,ClientCategory,SampleFormParameterFormulaCalculate
from websocket import frontend_setting
from account.models import CustomUser


@receiver(pre_save, sender=SampleFormParameterFormulaCalculate)
def SampleFormParameterFormulaCalculatePreSave(sender, instance, **kwargs):
    sample_form_obj = instance.sample_form    
    

@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterPreSave(sender, instance, **kwargs):
    instance.status = "processing"
    sample_form_obj = instance.sample_form
    sample_form_obj.status = "processing"
    sample_form_obj.save()
    # if not instance.pk:
    #     instance.status = "processing"
  
@receiver(pre_save, sender=ClientCategory)
def ClientCategoryPreSave(sender, instance, **kwargs):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    #start

    notification_message = "A client Category has created"
    path = frontend_setting.client_category
    from_notification = "admin"
    model_name = "ClientCategory"
    to_notification = "all_admin"
    is_read = False
    group_notification = "all_admin"


    
    #end
    # Send the notification message to the user's channel
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin',
        {
            'type': 'group.message',
            'message': notification_message
        }
    )

@receiver(pre_save, sender=CustomUser)
def CustomUserPreSave(sender, instance, **kwargs):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    #start

    notification_message = "A new user has been created"
    path = frontend_setting.client_category
    from_notification = "user"
    model_name = "CustomUser"
    to_notification = "all_admin"
    is_read = False
    group_notification = "all_admin"


    
    #end
    # Send the notification message to the user's channel
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        'admin',
        {
            'type': 'group.message',
            'message': notification_message
        }
    )