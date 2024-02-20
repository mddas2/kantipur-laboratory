from rest_framework import serializers
from django.contrib.auth.models import Group,Permission
from account.models import CustomUser,CustomUserImages,UserHaveInspector
from offices.models import Branches
from django.contrib.auth.hashers import make_password
from account import roles

class BranchReadSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "BranchReadSerializer"
        model = Branches
        fields = '__all__'

class UserHaveReadInspectorSerializer(serializers.ModelSerializer):
    branch = BranchReadSerializer(read_only = True)
    class Meta:
        ref_name = "UserHaveReadInspectorSerializer"
        model = UserHaveInspector
        fields = '__all__'

class UserHaveWrirteInspectorSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "UserHaveWrirteInspectorSerializer"
        model = UserHaveInspector
        fields = '__all__'

    def validate_branch(self,value):
        user = self.context['request'].user
        if user.role==roles.SUPERADMIN:
            return value
        else:
            raise serializers.ValidationError("You have not permission to update branch") 
    
    def validate_inspector_type(self,value):
        user = self.context['request'].user
        if user.role==roles.SUPERADMIN:
            return value
        else:
            raise serializers.ValidationError("You have not permission to update inspector type") 
    
    def validate_government_id(self,value):
        user = self.context['request'].user
        if user.role==roles.SUPERADMIN:
            return value
        else:
            raise serializers.ValidationError("You have not permission to update government id") 
    
    def validate_government_issued_document(self,value):
        user = self.context['request'].user
        if user.role==roles.SUPERADMIN:
            return value
        else:
            raise serializers.ValidationError("You have not permission to update issued document") 

class CustomUserImageSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "CustomUserImageSerializer"
        model = CustomUserImages
        fields = '__all__'

class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "ApprovedBySerializer_account"
        model = CustomUser
        fields = ['first_name','last_name','id','email','role','username'] 

class CustomUserListSerializer(serializers.ModelSerializer):

     class Meta:
        ref_name =  "account serializers"
        model = CustomUser
        fields = ['id','email','phone','username','first_name','last_name','remarks','date_joined','role','is_active','is_recheck','is_reject'] 


class CustomUserRetrieveSerializer(serializers.ModelSerializer):
    custom_user_image = CustomUserImageSerializer(many = True,read_only = True)
    approved_by = ApprovedBySerializer(read_only = True)
    inspector = UserHaveReadInspectorSerializer(many = False,read_only = False)
    class Meta:
        ref_name =  "account serializers"
        model = CustomUser
        exclude = ['password']
     
class CustomUserReadAssignedSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name =  "CustomUserReadAssignedSerializer"
        model = CustomUser
        fields = ['id','first_name','last_name','test_type','role'] 

class CustomUserReadLimitedSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name =  "CustomUserReadLimitedSerializer serializers"
        model = CustomUser
        fields = ['id','email','first_name','username'] 

class userAdminLevelDataSerializer(serializers.ModelSerializer):
     class Meta:
        ref_name =  "CustomUserReadLimitedSerializer2 serializers"
        model = CustomUser
        fields = ['id','email','first_name','username','last_name','position'] 


class CustomUserSerializer(serializers.ModelSerializer):
    
    def validate_password(self,value):#field level validation
        if len(value) < 2:
            raise serializers.ValidationError('Password must be 8 digit')
        return make_password(value) 
    
    def validate_test_types(self,value):#field level validation
        if value != None:         
            string = [int(id) for id in value.split(',')]
            initial_data = self.initial_data
            if initial_data.get('role') == str(roles.ANALYST) and len(string) <2:
                return string
            elif initial_data.get('role') == str(roles.SUPERVISOR):
                return string
            else:
                if initial_data.get('role') == str(roles.ANALYST):
                    raise serializers.ValidationError('multiple test type not alowed')
                else:
                    raise serializers.ValidationError('Test type allowed for only analyst and supervisor.') 
        return value
      
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
        # print(attrs,"\n attrs...")
        request = self.context.get('request')
        action = self.context['view'].action     

        if action == 'partial_update' and 'is_verified' in attrs and 'remarks' in attrs:
            attrs['approved_by'] = request.user

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
        # fields = '__all__' 
        exclude = ['test_type']


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
