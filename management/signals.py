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

    from management.models import SampleForm
    SampleForm.objects.filter(id=sample_form_obj.id).update(status=status)
    # sample_form_has_parameter.update(status=status)


# @receiver(pre_save, sender=SampleForm)
# def SampleForm(sender, instance, **kwargs):
#     parameter = sender.parameters.all()
#     print(parameter.count())
#     if not parameter.count() >=1:
#         print("parameter is null")
#     else:
#         print("parameter is not null ")


@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterPreSave(sender, instance, **kwargs):
    if not instance.pk:
        instance.status = "processing"
        sample_form_obj = instance.sample_form
        sample_form_obj.status = "processing"
        sample_form_obj.save()
    