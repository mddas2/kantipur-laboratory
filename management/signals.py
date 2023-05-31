# signals.py

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm,ClientCategory,SampleFormParameterFormulaCalculate
from websocket import frontend_setting
from account.models import CustomUser


@receiver(post_save, sender=SampleFormParameterFormulaCalculate)
def SampleFormParameterFormulaCalculatePreSave(sender, instance,created, **kwargs):
    
    sample_form_obj = instance.sample_form    
    parameter_obj = instance.parameter
    sample_form_has_parameter = SampleFormHasParameter.objects.filter(sample_form_id = sample_form_obj.id,parameter = parameter_obj.id)
    # check_parameter = sample_form_has_parameter.first().parameter.all()

    # print(check_parameter)
    status = "processing"
    
    parameters = sample_form_obj.parameters.all()    
    for param in parameters:
        formula_calculate_object = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id = sample_form_obj.id,parameter = param.id)
        if formula_calculate_object.exists():
            status = "completed"
        else:
            status = "processing"
            break

    sample_form = SampleForm.objects.get(id = sample_form_obj.id)
    if status == "completed":        
        sample_form.status = status
        sample_form.save() 
        # instance.status = status
        # instance.save()
    else:
        sample_form.status = status
        sample_form.save()
        # instance.status = status
        # instance.save()  

@receiver(pre_save, sender=SampleForm)
def SampleForm(sender, instance, **kwargs):
    parameter = sender.parameters.all()
    print(parameter.count())
    if not parameter.count() >=1:
        print("parameter is null")
    else:
        print("parameter is not null ")


@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterPreSave(sender, instance, **kwargs):
    if not instance.pk:
        instance.status = "processing"
        sample_form_obj = instance.sample_form
        sample_form_obj.status = "processing"
        sample_form_obj.save()
    
  
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