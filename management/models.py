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
    amendments = models.CharField(max_length=255)
    
    language = models.CharField(max_length=10)
    note = models.TextField()
    commodity_id = models.ForeignKey(Commodity,related_name="sample_form",on_delete=models.CASCADE,default=None)
    supervisor_user = models.ForeignKey(CustomUser, related_name="sample_has_parameters",default=None,on_delete=models.SET_NULL,null=True)
    parameters = models.ManyToManyField(TestResult, related_name="sample_form")

    status_choices = (
        ('pending', 'pending'),
        ('approved','approved'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('reject', 'reject'),
    )
    status = models.CharField(choices=status_choices, blank=True, null=True, max_length=155)

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
    
class SampleFormHasParameter(models.Model):#sample form has parameter and parameter for each parameter each analyst
    sample_form = models.ForeignKey(SampleForm,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,null=True)
    commodity = models.ForeignKey(Commodity,related_name="sample_has_parameter_analyst",on_delete=models.CASCADE,null=True)

    analyst_user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,default=None)
       
    parameter = models.ManyToManyField(TestResult, related_name="sample_has_parameters")
    
    status_choices = (
        ('pending', 'pending'),
        ('approved','approved'),
        ('processing', 'processing'),
        ('completed', 'completed'),
        ('reject', 'reject'),
    )
    status = models.CharField(choices=status_choices, blank=True, null=True, max_length=155)

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
    parameter = models.OneToOneField(TestResult, on_delete=models.CASCADE,null=True)
    result =  models.IntegerField(null=True)
    input_fields_value = models.CharField(max_length=2000,null=True)
    auto_calculate_result = models.CharField(max_length=200,null=True)
    remark = models.CharField(max_length=200,null=True)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(default=timezone.now)

