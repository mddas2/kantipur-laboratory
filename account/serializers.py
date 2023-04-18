from django.contrib.auth.models import Group,Permission
from .models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'   
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  



 


