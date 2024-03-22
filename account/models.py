from django.db import models
# from management.models import ClientCategory

# Create your models here.s
from django.db import models
from django.contrib.auth.models import AbstractUser
from offices.models import Branches,InspectorType
from .role_choices import ROLE_CHOICES

class TestType(models.Model):
    name = models.CharField(choices=(('Chemical','Chemical'),('Microbiological','Microbiological'),('Instrumental','Instrumental')), default=None, max_length=155,null=True)

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=15 , unique=True)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=255,unique=True)  
    nepali_name = models.CharField(max_length = 50,null = True,blank = True)

    test_type = models.ManyToManyField(TestType, related_name="users",default=None) 
    test_types = models.CharField(max_length=255,null=True)

    renew_document = models.FileField(upload_to='media/user/renew_doument',default=None)
    registration_document = models.FileField(upload_to='media/user/registration',default=None)
     
    department_name = models.CharField(max_length=255,null=True) 
    department_address =  models.CharField(max_length=60,default=None,null=True)#s
    registration_number = models.CharField(max_length=255,null=True) 

    # department_type = models.CharField(max_length=60, choices=department_type.department_code,default=None)#  

    is_active = models.BooleanField(default=True)

    is_verified = models.IntegerField(choices=[(0, 'Not verified'), (1, 'Verified')], default=0)
    approved_by = models.ForeignKey("CustomUser",related_name="user_approved",null=True,on_delete=models.SET_NULL)
    approved_date = models.DateField(null=True)

    is_recheck = models.BooleanField(default=False)
    is_reject = models.BooleanField(default=False)
    is_email_verified =  models.BooleanField(default=False) #for email verification.

    client_category = models.ForeignKey("management.ClientCategory",related_name="user",on_delete=models.CASCADE,null=True) 
    importer_name = models.CharField(max_length=255,null=True) 
    importer_address = models.CharField(max_length=255,null=True) 
    other_detail = models.CharField(max_length=255,null=True) 


    created_by = models.IntegerField(null=True)
    remarks = models.CharField(max_length=200,null=True)

    position = models.CharField(max_length=200,null=True) #post 
    position_nepali = models.CharField(max_length=200,null=True,blank = True)

    created_date = models.DateTimeField(auto_now_add=True)  
    updated_date = models.DateTimeField(auto_now=True)
    
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, blank=True, null=True)
    is_public_analyst = models.BooleanField(default = False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    @property
    def getRoleName(self):
        if self.role==1:
            return 'Superadmin'
        elif self.role==2:
            return 'Smu'
        elif self.role==3:
            return 'Supervisor'
        elif self.role==4:
            return 'Analyst'
        elif self.role==6:
            return 'Verifier'
        elif self.role==7:
            return 'Admin'
        else:
            return 'None'
    
    @property
    def get_full_name(self):
        return str(self.first_name) + " " + str(self.last_name)

    def save(self, *args, **kwargs):
        if self.pk is None:
            # New instance, set is_active to False by default
            self.is_active = True

            super().save(*args, **kwargs)
            if self.test_types != None:
                self.test_type.set(self.test_types)
                
        else:
            if self.test_types != None:
                try:
                    self.test_type.set(self.test_types)
                    #print("blunder error account")
                except:
                    pass                

            super().save(*args, **kwargs)

        return self


class CustomUserImages(models.Model):
    file = models.FileField(upload_to='media/user/customuserimages',default=None)
    name = models.CharField(max_length=255,null=True)
    user = models.ForeignKey(CustomUser,related_name="custom_user_image",null=True,on_delete=models.CASCADE)

class UserHaveInspector(models.Model):
    user = models.OneToOneField(CustomUser,related_name = "inspector", on_delete = models.CASCADE)
    branch = models.ForeignKey(Branches,on_delete = models.SET_NULL , null = True,blank = True)
    inspector_type = models.ManyToManyField(InspectorType)
    nepali_name = models.CharField(max_length = 200)
    government_id = models.CharField(max_length = 300)
    government_issued_document = models.FileField(upload_to='media/user/inspector',blank=True,null=True)

