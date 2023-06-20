# signals.py

from django.db.models.signals import pre_save,post_save
from django.dispatch import receiver
from management.models import SampleFormHasParameter,SampleForm,ClientCategory,SampleFormParameterFormulaCalculate,SampleFormVerifier
from websocket import frontend_setting
from account.models import CustomUser
from django.db import transaction
from django.db.models.signals import m2m_changed
# from datetime import datetime
from django.utils import timezone
from websocket.handle_notification import sampleFormNotificationHandler

@receiver(post_save, sender=SampleFormParameterFormulaCalculate)
def SampleFormParameterFormulaCalculatePreSave(sender, instance,created, **kwargs):
    
    sample_form_obj = instance.sample_form    
    parameter_obj = instance.parameter

    sample_form_has_parameter = SampleFormHasParameter.objects.filter(sample_form_id = sample_form_obj.id,parameter = parameter_obj.id)   
    if sample_form_has_parameter.first().status == "pending":
        sampleFormNotificationHandler(instance,"update","SampleFormHasParameter","Analyst started testing sample form "+instance.id ,"particular message ","SUPERVISOR","ANALYST from message")
        sample_form_has_parameter.update(status="processing")
        
    
@receiver(pre_save, sender=SampleForm)
def handle_sampleform_presave(sender, instance, **kwargs):
    original_sample_form = None
    if not instance.pk:
        sampleFormNotificationHandler(instance,"create","SampleForm","new sample form creating ","particular message ","USER_ADMIN","USER to message")
    if instance.id:
        original_sample_form = SampleForm.objects.get(pk=instance.id).supervisor_user
    if instance.supervisor_user != original_sample_form:
        instance.status = "not_assigned"
        sampleFormNotificationHandler(instance,"create","SampleForm","assigned to supervisor new sample form update ","particular message ","ADMIN_SUPERVISOR","ADMIN")
        instance.approved_date = timezone.now()
            
             

@receiver(m2m_changed, sender=SampleFormHasParameter.parameter.through)
def sample_form_has_parameter_m2m_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    sample_form_obj = instance.sample_form    

    instance.is_supervisor_sent = False #blunder error fixed
    instance.status="processing"
    instance.save()

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

        well = 0
        for parame in sample_form_obj.parameters.all():
            sample_form_has_parame_obj =  SampleFormHasParameter.objects.filter(sample_form = sample_form_obj.id,parameter=parame)
            if sample_form_has_parame_obj.exists():
                well = 1
            else:
                well = 0
                break
        
        
        sample_form_status = "processing"
        for obj in sample_form_has_parameter_obj:
            if obj.is_supervisor_sent == True:
                sample_form_has_param = SampleFormHasParameter.objects.filter(id=instance.id)
                sample_form_has_param.update(status = "completed")

                sample_form_has_parameters_analyst_parameters = obj.parameter.all()
                for pram in sample_form_has_parameters_analyst_parameters:
                    formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(sample_form = sample_form_obj.id,parameter_id = pram.id)
                    formula_calculate.update(status="completed")

                sample_form_status = "not_verified"
                is_analyst_test = True
            else:
                is_analyst_test = False
                sample_form_status = "processing"
                break
        if well == 1:
            SampleForm.objects.filter(id=sample_form_obj.id).update(is_analyst_test = is_analyst_test,status=sample_form_status)
        else:
            print("all parameter has not assigned...")
        
  

@receiver(pre_save, sender=SampleFormHasParameter)
def SampleFormHasParameterAfterSave(sender, instance , **kwargs):
    if not instance.pk:
        instance.status = "pending"
        sampleFormNotificationHandler(instance,"create","SampleFormHasParameter","assigned to analyst","particular message ","SUPERVISOR","All admin except verifier")
        
   
@receiver(pre_save, sender=SampleFormVerifier)
def SampleFormHasVerifierPreSave(sender, instance, **kwargs):
    sample_form_obj = instance.sample_form
    if not instance.pk:  
        sample_form_obj.form_available = "verifier"
        sample_form_obj.status = "not_verified"
        sample_form_obj.save()
    else:        
        if instance.is_verified == True:
            sample_form_obj.status = "completed"
            sample_form_obj.completed_date = timezone.now()
            sample_form_obj.save()


