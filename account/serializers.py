from rest_framework import serializers
from management.serializers import ClientCategorySerializer
from django.contrib.auth.models import Group,Permission
from account.models import CustomUser
from django.contrib.auth.hashers import make_password

class CustomUserSerializer(serializers.ModelSerializer):
    # client_category = ClientCategorySerializer(read_only=True)
    
    def validate_password(self,value):#field level validation
        if len(value) < 2:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value)   
    
    class Meta:
        model = CustomUser
        fields = '__all__'   
        
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'  

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'  

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()




 


