from django.db import models
from django.db.models import UniqueConstraint
from account.models import CustomUser
from django.utils import timezone
from . import encode_decode

class ClientCategory(models.Model):
    name = models.CharField(max_length=255,unique=True)
    # address = models.CharField(max_length=255)
    # reg_no = models.CharField(max_length=255)
    # registration_document = models.ImageField(upload_to='media/client_category', null=True)
    # user_renew_document = models.ImageField(upload_to='media/client_category', null=True)
    

class CommodityCategory(models.Model):
    name = models.CharField(max_length=255,unique=True) 
    name_nepali = models.CharField(max_length=255,null=True) 
    
class Commodity(models.Model):
    #type_test = choice 
    category = models.ForeignKey(CommodityCategory,related_name="commodity",on_delete=models.CASCADE,null=True) 
    name = models.CharField(max_length=255,null=False,unique=True)
    name_nepali = models.CharField(max_length=255,null=True)
    test_duration = models.CharField(max_length=255,null=True)
    units = models.CharField(max_length=255,null=True)
    price = models.IntegerField(null=True)    
    
class TestResult(models.Model):
    commodity = models.ForeignKey(Commodity,related_name="test_result",on_delete=models.CASCADE,null=True)
    formula = models.CharField(max_length=255, null=True)
    formula_notation = models.TextField(max_length=1000,null=True)
    name = models.CharField(max_length=255,null=False) #parameter name
    name_nepali = models.CharField(max_length=255,null=True) #parameter name
    test_type = models.CharField(choices=(('Chemical','Chemical'),('Instrumental','Instrumental'),('Microbiological','Microbiological')), default=None, max_length=155,null=True)
    test_type_nepali = models.CharField(max_length=255,null=True)
    ref_test_method = models.CharField(max_length=255,null=True)
    units = models.CharField(max_length=100,null=True)
    units_nepali = models.CharField(max_length=100,null=True)
    price = models.IntegerField(null=True)
    results = models.CharField(max_length=100,null=True)
    mandatory_standard = models.CharField(max_length=100,null=True)
    mandatory_standard_nepali = models.CharField(max_length=100,null=True)

    remarks = models.TextField(max_length=500,null=True)    

class SampleForm(models.Model):#ClientRequest
    owner_user = models.EmailField(max_length=100,null=False,default=None)
    name = models.CharField(max_length=255, null=True)
    condition = models.CharField(max_length=255)
    mfd = models.DateField()
    dfb = models.DateField()
    batch = models.IntegerField()
    brand = models.CharField(max_length=255)
    purpose = models.CharField(max_length=255)
    requested_export = models.CharField(max_length=155,null=True)
    report_date = models.DateField()
    amendments = models.CharField(max_length=255,null=True,blank=True)
    is_commodity_select = models.BooleanField(default=False) #if parameter not select then auto select parameter.this insure that commodity select or parameter.
    language = models.CharField(max_length=10)
    note = models.TextField(null=True,blank=True)
    commodity = models.ForeignKey(Commodity,related_name="sample_form",on_delete=models.CASCADE,default=None)
    supervisor_user = models.ForeignKey(CustomUser, related_name="sample_has_parameters",default=None,on_delete=models.SET_NULL,null=True)
    parameters = models.ManyToManyField(TestResult, related_name="sample_form",blank=True)

    approved_by = models.ForeignKey(CustomUser, related_name="sample_form_approve",on_delete=models.SET_NULL,null=True) #smu
    approved_date = models.DateTimeField(null=True)
    completed_date = models.DateTimeField(null=True)

    user_encode_id = models.CharField(max_length=255, blank=True, null=True)
    supervisor_encode_id = models.CharField(max_length=255, blank=True, null=True)
    analyst_encode_id = models.CharField(max_length=255, blank=True, null=True)
    verifier_encode_id = models.CharField(max_length=255, blank=True, null=True)

    
    remarks = models.CharField(max_length=1000,null=True)
    remarks_recheck_verifier = models.CharField(max_length=1000,null=True)
    remarks_reject_verifier = models.CharField(max_length=1000,null=True)

    verified_by = models.ForeignKey(CustomUser, related_name="sample_form_verified_by",on_delete=models.SET_NULL,null=True) #verifier


    is_analyst_test = models.BooleanField(default=False) #if in paramater_has_analyst send to supervisor then this.from all param then True

    status_choices = (
        ('pending', 'pending'),#initial
        ('processing', 'processing'), #smu-assign-supervisor (smu:pending-not_assign,display:processing)
        ('not_assigned', 'not_assigned'),#supervisor-assign-analyst (supervisor:not_assign-processing,display:processing)
        ('not_verified', 'not_verified'),#analyst-to-supervisor(supervisor:processing-not_verified,display:not_verified)
        ('verified', 'verified'),
        ('completed', 'completed'),#supervisor-assign-verifier (supervisor:not_verified-verified,display:processing) action:recheck,reject
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
    )
    status = models.CharField(choices=status_choices, blank=True, null=True, max_length=155)

    SUPERADMIN = "superadmin"
    SMU = "smu"
    SUPERVISOR = "supervisor"
    ANALYST = "analyst"
    USER = "user"
    VERIFIER = "verifier"

    ROLE_CHOICES = (
        (SUPERADMIN, 'superadmin'),
        (SMU,'smu'),
        (SUPERVISOR, 'supervisor'),
        (ANALYST, 'analyst'),
        (USER, 'user'),
        (VERIFIER,'verifier'),
    )

    form_available = models.CharField(max_length=100,choices=ROLE_CHOICES, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        create = False
        if not self.pk:
            # Generate and save the encoded IDs for all user roles
            create = True
           
        super().save(*args, **kwargs)
        if create == True:
            self.user_encode_id = encode_decode.generateEncodeIdforSampleForm(self.pk, "user")
            self.supervisor_encode_id = encode_decode.generateEncodeIdforSampleForm(self.pk, "common")
            self.analyst_encode_id = encode_decode.generateEncodeIdforSampleForm(self.pk, "common")
            self.verifier_encode_id = encode_decode.generateEncodeIdforSampleForm(self.pk, "common")
            self.save()

class SuperVisorSampleForm(models.Model):#sample form has parameter and parameter for each parameter each suspervisor
    sample_form = models.ForeignKey(SampleForm,related_name="supervisor_sample_form",on_delete=models.CASCADE,null=True)
    supervisor_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
       
    parameters = models.ManyToManyField(TestResult, related_name="supervisor_has_parameter")
    test_type = models.CharField(max_length=1000,null=True)

    is_supervisor_sent = models.BooleanField(default=False)
    is_analyst_test = models.BooleanField(default=False)
    
    status_choices = (       
        ('pending', 'pending'), 
        ('not_assigned', 'not_assigned'), 
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
        ('not_verified','not_verified'),
        ('tested','tested'),
        ('verified','verified'),
    )
    status = models.CharField(choices=status_choices,default="not_assigned" , blank=True, null=True, max_length=155)

    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=1000,null=True)


class SampleFormHasParameter(models.Model):#sample form has parameter and parameter for each parameter each analyst
    sample_form = models.ForeignKey(SampleForm,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,null=True)
    super_visor_sample_form = models.ForeignKey(SuperVisorSampleForm,related_name="sample_has_parameter_analyst", on_delete=models.CASCADE,null=True)
    commodity = models.ForeignKey(Commodity,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,default=None)

    analyst_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
       
    parameter = models.ManyToManyField(TestResult, related_name="sample_has_parameters")

    is_supervisor_sent = models.BooleanField(default=False)
    
    status_choices = (       
        ('pending', 'pending'), 
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('recheck', 'recheck'),
        ('rejected', 'rejected'),
        ('not_verified','not_verified'),
        ('tested','tested'),
        ('verified','verified')
    )
    status = models.CharField(choices=status_choices,default="pending" , blank=True, null=True, max_length=155)

    SUPERADMIN = "superadmin"
    SMU = "smu"
    SUPERVISOR = "supervisor"
    ANALYST = "analyst"
    USER = "user"

    ROLE_CHOICES = (
        (SUPERADMIN, 'superadmin'),
        (SMU,'smu'),
        (SUPERVISOR, 'supervisor'),
        (ANALYST, 'analyst'),
        (USER, 'user'),
    )

    form_available = models.CharField(max_length=100,choices=ROLE_CHOICES, blank=True, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)
    remarks = models.CharField(max_length=1000,null=True)


    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['sample_form', 'parameter'], name='unique_parameter_per_sample_form'),
    #         UniqueConstraint(fields=['sample_form', 'analyst_user'], name='unique_analyst_per_sample_form'),
    #         UniqueConstraint(fields=['sample_form', 'supervisor_user'], name='unique_supervisoruser_per_sample_form')
    #     ]

class Payment(models.Model):
    sample_form = models.ForeignKey(SampleForm,related_name='payment' , on_delete=models.DO_NOTHING)
    owner_email = models.EmailField(max_length=100,null=True)
    voucher_number = models.CharField(blank=True, null=True, max_length=155)
    register_date = models.CharField(blank=True, null=True, max_length=155)
    amount = models.IntegerField(blank=True, null=True)
    payment_receipt = models.FileField(upload_to='uploads/receipt',null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

class SampleFormParameterFormulaCalculate(models.Model):
    sample_form = models.ForeignKey(SampleForm,related_name="result",on_delete=models.CASCADE,null=True)
    sample_form_has_parameter = models.ForeignKey(SampleFormHasParameter,related_name="formula_calculate",on_delete=models.CASCADE,default=None,null=True)
    commodity = models.ForeignKey(Commodity,on_delete=models.CASCADE,null=True)
    parameter = models.ForeignKey(TestResult, on_delete=models.CASCADE,null=True)
    result =  models.FloatField(null=True)
    is_verified = models.BooleanField(default=False)
    input_fields_value = models.CharField(max_length=2000,null=True)
    auto_calculate_result = models.CharField(max_length=200,null=True)
    remarks = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    status_choices = (
        ('pending', 'pending'),
        ('rejected', 'rejected'),
        ('recheck', 'recheck'),       
        ('completed', 'completed'),
        ('tested','tested'),
        ('processing', 'processing'),
    )
    status = models.CharField(choices=status_choices, default="processing", max_length=155)


class SampleFormVerifier(models.Model):
    sample_form = models.OneToOneField(SampleForm,related_name="verifier",on_delete=models.CASCADE,default=None)
    is_verified = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    remarks = models.CharField(max_length=1000,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

class RawDataSheet(models.Model):
    sample_form = models.ForeignKey(SampleForm,related_name="raw_datasheet",on_delete=models.CASCADE,default=None)
    sample_form_has_parameter = models.ForeignKey(SampleFormHasParameter,related_name="raw_datasheet",on_delete=models.CASCADE,default=None)
    super_visor_sample_form = models.ForeignKey(SuperVisorSampleForm,related_name="raw_datasheet", on_delete=models.CASCADE,null=True)
    test_type = models.CharField(max_length=2000,null=True)
    status = models.CharField(max_length=2000,null=True)
    analyst_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
    remarks = models.CharField(max_length=1000,null=True)
    supervisor_remarks = models.CharField(max_length=1000,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    
class RawDataSheetDetail(models.Model):
    raw_data = models.ForeignKey(RawDataSheet, on_delete=models.CASCADE,related_name="raw_data",null=True)
    parameter = models.ForeignKey(TestResult, on_delete=models.CASCADE,null=True)
    result =  models.FloatField(null=True)
    is_verified = models.BooleanField(default=False)
    input_fields_value = models.CharField(max_length=2000,null=True)
    auto_calculate_result = models.CharField(max_length=200,null=True)
    remark = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)



