from rest_framework import serializers
from management.serializers import ClientCategorySerializer
from django.contrib.auth.models import Group,Permission
from account.models import CustomUser
from django.contrib.auth.hashers import make_password
from management import roles


class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "ApprovedBySerializer_account"
        model = CustomUser
        fields = '__all__' 

class CustomUserSerializer(serializers.ModelSerializer):
    # client_category = ClientCategorySerializer(read_only=True)
    
    def validate_password(self,value):#field level validation
        if len(value) < 2:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value) 
      
    def validate_role(self,value):#field level validation
        user = self.context['request'].user
        if not user.is_authenticated:
            if value!=roles.USER:
                raise serializers.ValidationError("You can only set USER as role") 
        elif user.role==roles.SUPERADMIN:
            return value
        elif user.is_authenticated and value!=roles.USER:
                raise serializers.ValidationError("You can only set USER as role") 
        return value

    def validate_is_superuser(self,value):
        if value == True:
            raise serializers.ValidationError("You can not set USER as superadmin") 
        else:
            return False
    
    def validate(self, attrs):
        request = self.context.get('request')
        action = self.context['view'].action        
        if action == 'partial_update':
            old_password = request.data.get('old_password')  
            if old_password is not None:      
                instance = self.instance
                if not instance.check_password(old_password):
                    raise serializers.ValidationError("Password does not match")
        return attrs
    
    approved_by = ApprovedBySerializer(read_only = True)
    class Meta:
        ref_name =  "account serializer"
        model = CustomUser
        fields = '__all__' 

class RoleSerializer(serializers.Serializer):
    role_id = serializers.IntegerField()
    role_name = serializers.CharField()
    def to_representation(self, instance):
        return {'role_id': instance[0], 'role_name': instance[1]}
    
class departmentTypeSerializer(serializers.Serializer):
    code = serializers.CharField()
    name = serializers.CharField()
    def to_representation(self, instance):
        return {'code': instance[0], 'name': instance[1]}

   
        
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
