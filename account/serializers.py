from rest_framework import serializers
from management.serializers import ClientCategorySerializer
from django.contrib.auth.models import Group,Permission
from account.models import CustomUser
from django.contrib.auth.hashers import make_password
from management import roles

class CustomUserSerializer(serializers.ModelSerializer):
    # client_category = ClientCategorySerializer(read_only=True)
    
    def validate_password(self,value):#field level validation
        if len(value) < 2:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value) 
      
    def validate_role(self,value):#field level validation
        user = self.context['request'].user
        if user.role==roles.SUPERADMIN:
            return value
        elif value!=roles.USER:
            raise serializers.ValidationError("You can only set USER") 
    
    class Meta:
        model = CustomUser
        fields = '__all__' 

class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    role_name = serializers.CharField()
    def to_representation(self, instance):
        return {'role_id': instance[0], 'role_name': instance[1]}

   
        
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
    username = serializers.CharField()
    password = serializers.CharField()

class GroupNamesSerializer(serializers.Serializer):
    group_names = serializers.ListField(child=serializers.CharField())

class PermissionGroupSerializer(serializers.Serializer):
    permission_id = serializers.IntegerField()
    groups = serializers.DictField(child=serializers.BooleanField())
