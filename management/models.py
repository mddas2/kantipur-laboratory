from django.db import models

class ClientCategory(models.Model):
    name = models.CharField(max_length=255)
    # address = models.CharField(max_length=255)
    # reg_no = models.CharField(max_length=255)
    # reg_document = models.ImageField(upload_to='media/client_category', null=True)
    # user_renew_document = models.ImageField(upload_to='media/client_category', null=True)
    
    
class SampleForm(models.Model):#ClientRequest
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
    commodity_id = models.IntegerField(null=True)
    parameter = models.CharField(max_length=255, null=True)
    
    
class Commodity(models.Model):
    #type_test = choice 
    category_id = models.IntegerField(null=True) 
    ref_test_method = models.CharField(max_length=255)
    units = models.CharField(max_length=255)
    mandatory_standard = models.CharField(max_length=255)
    remarks = models.TextField()
    
    
class TestResult(models.Model):
    commodity_id = models.IntegerField(null=True)
    parameter = models.CharField(max_length=255)
    ref_test_method = models.CharField(max_length=255)
    units = models.CharField(max_length=100)
    results = models.CharField(max_length=100)
    mandatory_standard = models.CharField(max_length=100)
    remarks = models.TextField()    

class CommodityCategory(models.Model):
    name = models.CharField(max_length=255)

    