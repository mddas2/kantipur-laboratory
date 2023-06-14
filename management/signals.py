# signals.py

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm,ClientCategory,SampleFormParameterFormulaCalculate,SampleFormVerifier
from websocket import frontend_setting
from account.models import CustomUser
from django.db import transaction
from django.db.models.signals import m2m_changed


@receiver(post_save, sender=SampleFormParameterFormulaCalculate)
def SampleFormParameterFormulaCalculatePreSave(sender, instance,created, **kwargs):
    
    sample_form_obj = instance.sample_form    
    parameter_obj = instance.parameter

    sample_form_has_parameter = SampleFormHasParameter.objects.filter(sample_form_id = sample_form_obj.id,parameter = parameter_obj.id)   
    if sample_form_has_parameter.first().status == "pending":
        sample_form_has_parameter.update(status="processing")
        
    
    


# @receiver(pre_save, sender=SampleForm)
# def SampleForm(sender, instance, **kwargs):
#     parameter = sender.parameters.all()
#     print(parameter.count())
#     if not parameter.count() >=1:
#         print("parameter is null")
#     else:
#         print("parameter is not null ")


@receiver(m2m_changed, sender=SampleFormHasParameter.parameter.through)
def sample_form_has_parameter_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    sample_form_obj = instance.sample_form    

    status = "not_assigned"
    
    parameters = sample_form_obj.parameters.all()

    for param in parameters:    
        sample_form_has_parameter_object = SampleFormHasParameter.objects.filter(sample_form = sample_form_obj,parameter = param.id)
        if sample_form_has_parameter_object.exists():
            status = "processing"
        else:
            status = "not_assigned"
            break
   
    print(status," look ")
    print(sample_form_obj.status," obj  status")
        
    sample_form_obj.status = status   
    sample_form_obj.save()

@receiver(post_save, sender=SampleFormHasParameter)
def SampleFormHasParameterAfterSave(sender, instance ,created , **kwargs):
    if instance.is_supervisor_sent == True:
        sample_form_obj = instance.sample_form
        sample_form_has_parameter_obj = SampleFormHasParameter.objects.filter(sample_form = sample_form_obj.id) 
        is_analyst_test = False
        sample_form_status = "processing"
        for obj in sample_form_has_parameter_obj:
            if obj.is_supervisor_sent == True:
                sample_form_has_param = SampleFormHasParameter.objects.filter(id=instance.id)
                sample_form_has_param.update(status = "completed")

                formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(sample_form = sample_form_obj.id)
                formula_calculate.update(status="completed")
                sample_form_status = "not_verified"
                is_analyst_test = True
            else:
                is_analyst_test = False
                sample_form_status = "processing"
                break
        print(is_analyst_test,"sd asd asad ") #if  sent to supervisor then set to is_analyst_test to 1 
        SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = is_analyst_test,status=sample_form_status)
     
  

@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterAfterSave(sender, instance , **kwargs):

    if not instance.pk:
        instance.status = "pending"
   
@receiver(pre_save, sender=SampleFormVerifier)
def SampleFormHasVerifierPreSave(sender, instance, **kwargs):
    sample_form_obj = instance.sample_form
    if not instance.pk:  
        sample_form_obj.form_available = "verifier"
        sample_form_obj.status = "not_verified"
        sample_form_obj.save()
    else:        
        print("update")
        if instance.is_verified == True:
            sample_form_obj.status = "completed"
            sample_form_obj.save()


