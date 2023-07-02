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

    # def to_internal_value(self, data):
    #     data = data.copy()
    #     if 'test_type' in data:
    #         print("test type  ",data['test_type'])
    #         ids_str = data['test_type']
    #         ids = [int(id_str) for id_str in ids_str.split(',') if id_str.isdigit()]
    #         data['test_type'] = ids
    #         print(ids)
    #     if 'client_category' in data:
    #         client_category = data['client_category']
    #         print(client_category)
    #         data['client_category_id'] = client_category

    #     return data

    
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

    def get_extra_kwargs(self):
        extra_kwargs = super().get_extra_kwargs()
        try:
            if self.context['request'].method == 'PUT':
                extra_kwargs['password'] = {'required': False}
            return extra_kwargs
        except:
            pass
    
    class Meta:
        ref_name =  "account serializer"
        model = CustomUser
        fields = '__all__' 
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        test_type = instance.test_type
        try:            
            string = [int(value) for value in test_type.split(',')]
        except:
            string = test_type
        #representation['test_type'] = string
        return representation


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
