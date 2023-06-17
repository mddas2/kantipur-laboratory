from django.db import models
from django.db.models import UniqueConstraint
from account.models import CustomUser
from django.utils import timezone

class ClientCategory(models.Model):
    name = models.CharField(max_length=255,unique=True)
    # address = models.CharField(max_length=255)
    # reg_no = models.CharField(max_length=255)
    # registration_document = models.ImageField(upload_to='media/client_category', null=True)
    # user_renew_document = models.ImageField(upload_to='media/client_category', null=True)
    

class CommodityCategory(models.Model):
    name = models.CharField(max_length=255,unique=True) 
    
class Commodity(models.Model):
    #type_test = choice 
    category = models.ForeignKey(CommodityCategory,related_name="commodity",on_delete=models.CASCADE,null=True) 
    name = models.CharField(max_length=255,null=False,unique=True)
    test_duration = models.IntegerField(null=True)
    units = models.CharField(max_length=255,null=True)
    price = models.IntegerField(null=True)    
    
class TestResult(models.Model):
    commodity = models.ForeignKey(Commodity,related_name="test_result",on_delete=models.CASCADE,null=True)
    formula = models.CharField(max_length=255, null=True)
    formula_notation = models.TextField(max_length=1000,null=True)
    name = models.CharField(max_length=255,null=False) #parameter name
    test_type = models.CharField(max_length=255,null=True)
    ref_test_method = models.CharField(max_length=255,null=True)
    units = models.CharField(max_length=100,null=True)
    price = models.IntegerField(null=True)
    results = models.CharField(max_length=100,null=True)
    mandatory_standard = models.CharField(max_length=100,null=True)
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
    report_date = models.DateField()
    amendments = models.CharField(max_length=255,null=True,blank=True)
    is_commodity_select = models.BooleanField(default=False) #if parameter not select then auto select parameter.this insure that commodity select or parameter.
    language = models.CharField(max_length=10)
    note = models.TextField(null=True,blank=True)
    commodity = models.ForeignKey(Commodity,related_name="sample_form",on_delete=models.CASCADE,default=None)
    supervisor_user = models.ForeignKey(CustomUser, related_name="sample_has_parameters",default=None,on_delete=models.SET_NULL,null=True)
    parameters = models.ManyToManyField(TestResult, related_name="sample_form",blank=True)

    approved_by = models.ForeignKey(CustomUser, related_name="sample_form_approve",on_delete=models.SET_NULL,null=True) #smu
    approved_date = models.DateField(null=True)
    completed_date = models.DateField(null=True)

    verified_by = models.ForeignKey(CustomUser, related_name="sample_form_verified_by",on_delete=models.SET_NULL,null=True) #verifier


    is_analyst_test = models.BooleanField(default=False) #if in paramater_has_analyst send to supervisor then this.from all param then True

    status_choices = (
        ('pending', 'pending'),#initial
        ('processing', 'processing'), #smu-assign-supervisor (smu:pending-not_assign,display:processing)
        ('not_assigned', 'not_assigned'),#supervisor-assign-analyst (supervisor:not_assign-processing,display:processing)
        ('not_verified', 'not_verified'),#analyst-to-supervisor(supervisor:processing-not_verified,display:not_verified)
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
    
class SampleFormHasParameter(models.Model):#sample form has parameter and parameter for each parameter each analyst
    sample_form = models.ForeignKey(SampleForm,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,null=True)
    commodity = models.ForeignKey(Commodity,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,null=True)

    analyst_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
       
    parameter = models.ManyToManyField(TestResult, related_name="sample_has_parameters")

    is_supervisor_sent = models.BooleanField(default=False)
    
    status_choices = (       
        ('pending', 'pending'), 
        ('processing', 'processing'),
        ('completed', 'completed'),
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

    # class Meta:
    #     constraints = [
    #         UniqueConstraint(fields=['sample_form', 'parameter'], name='unique_parameter_per_sample_form'),
    #         UniqueConstraint(fields=['sample_form', 'analyst_user'], name='unique_analyst_per_sample_form'),
    #         UniqueConstraint(fields=['sample_form', 'supervisor_user'], name='unique_supervisoruser_per_sample_form')
    #     ]

class Payment(models.Model):
    sample_form = models.OneToOneField(SampleForm,related_name='payment' , on_delete=models.DO_NOTHING)
    owner_email = models.EmailField(max_length=100,null=True)
    voucher_number = models.CharField(blank=True, null=True, max_length=155)
    register_date = models.CharField(blank=True, null=True, max_length=155)
    ammount = models.IntegerField(blank=True, null=True)
    payment_receipt = models.FileField(upload_to='uploads/receipt',null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

class SampleFormParameterFormulaCalculate(models.Model):
    sample_form = models.ForeignKey(SampleForm,related_name="result",on_delete=models.CASCADE,null=True)
    commodity = models.ForeignKey(Commodity,on_delete=models.CASCADE,null=True)
    parameter = models.ForeignKey(TestResult, on_delete=models.CASCADE,null=True)
    result =  models.FloatField(null=True)
    is_verified = models.BooleanField(default=False)
    input_fields_value = models.CharField(max_length=2000,null=True)
    auto_calculate_result = models.CharField(max_length=200,null=True)
    remark = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

    status_choices = (
        ('pending', 'pending'),       
        ('completed', 'completed'),
        ('processing', 'processing'),
    )
    status = models.CharField(choices=status_choices, default="processing", max_length=155)


class SampleFormVerifier(models.Model):
    sample_form = models.OneToOneField(SampleForm,related_name="verifier",on_delete=models.CASCADE,default=None)
    is_verified = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)




