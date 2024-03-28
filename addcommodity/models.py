# from django.db import models

# # Create your models here.
# class AddCommodity(models.Model):
#     name = models.CharField(max_length=100,null=True)
#     description = models.TextField(null=True)
#     parameters = models.CharField(max_length=100,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
    

# class ParameterDetails(models.Model):
#     commodity_category = models.CharField(max_length=100,null=True)
#     commodity_name = models.CharField(max_length=100,null=True)
#     commodity_price = models.CharField(max_length=100,null=True)
    
#     parameter_name = models.CharField(max_length=100,null=True)
#     parameter_value = models.CharField(max_length=100,null=True)
#     unit_of_measurement = models.CharField(max_length=100,null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.commodity_category

