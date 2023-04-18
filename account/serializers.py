from django.contrib.auth.models import Group,Permission
from .models import CustomUser
from rest_framework import serializers


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'  

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  

class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'   

 


