from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter,SuperVisorSampleForm,ClientCategoryDetail,TestResult
from account.models import CustomUser
from rest_framework import serializers
from account import roles
from management.encode_decode import generateAutoEncodeIdforSampleForm
from management.status_naming import over_all_status

# class ClientCategoryDetailImagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         ref_name = "ClientCategoryDetailImagesSerializer"
#         model = ClientCategoryDetailImages
#         fields = '__all__'

class TestResultParametersSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "TestResultforCompletedSampleFormHasVerifierSerializer_User"
        model = TestResult
        fields = ['name']

class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    client_category_name = serializers.SerializerMethodField()
    class Meta:
        ref_name = "ClientCategoryDetailSerializer"
        model = ClientCategoryDetail
        fields = ['client_category_name']
    
    def get_client_category_name(self,obj):
        return obj.client_category.name

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_report_finalserializer"
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CustomUserSuperVisorUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_report_finalserializer"
        model = CustomUser
        fields = ['first_name','last_name'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_report_finalserializer"
        model = Commodity
        fields = ['name']

class SupervisorSampleFormSerializer(serializers.ModelSerializer):
    supervisor_user = CustomUserSuperVisorUserSerializer(read_only = True)
    class Meta:
        ref_name = "SupervisorSampleFormSerializer"
        model = SuperVisorSampleForm
        fields = ['supervisor_user']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "SampleFormHasParameter_final_report"
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class FinalSampleFormReportSerializer(serializers.ModelSerializer):
    # sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only = True)
    id = serializers.SerializerMethodField()

    client_category_detail = ClientCategoryDetailSerializer(read_only = True)
    
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    class Meta:
        name = "FinalSampleFormReportAPIViewReport"
        model = SampleForm
        fields = ['id','supervisor_sample_form','name','commodity','status','created_date','completed_date','client_category_detail','namuna_code','is_print','verified_date','approved_date'] #user access
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')

        status = representation.get('status')
        if request.user.role == roles.SUPERVISOR:
            
            if status == "completed":
                stat = "verified"
                representation['status'] = stat
            else:
                representation['status'] = over_all_status[status]
        else:
            representation['status'] = over_all_status[status]

        return representation

class FinalSampleFormReportSerializer_User(serializers.ModelSerializer):
    # sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only = True)
    id = serializers.SerializerMethodField()
    parameters = TestResultParametersSerializer(many=True,read_only = True)
    client_category_detail = ClientCategoryDetailSerializer(read_only = True)
    
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    class Meta:
        name = "FinalSampleFormReportAPIView_User_Report"
        model = SampleForm
        fields = ['id','supervisor_sample_form','name','commodity','status','created_date','completed_date','client_category_detail','namuna_code','mfd','dfb','sample_quantity','sample_units','voucher_number','voucher_date','analysis_fee','parameters','days_dfb','dfb_duration'] #user access
    
    def to_representation(self,instance):
        representation = super().to_representation(instance)
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        return representation

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')

        status = representation.get('status')
        if request.user.role == roles.SUPERVISOR:
            
            if status == "completed":
                stat = "verified"
                representation['status'] = stat
            else:
                representation['status'] = over_all_status[status]
        else:
            representation['status'] = over_all_status[status]

        return representation

class AssignedSampleForSmuSuperAdminSerializer(serializers.ModelSerializer):
    # sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only=True)
    client_category_detail = serializers.SerializerMethodField()#ClientCategoryDetailSerializer(read_only = True)
    class Meta:
        name = "AssignedSampleForSmuSuperAdminSerializer"
        model = SampleForm
        fields = ['id','supervisor_sample_form','name','commodity','status','created_date','refrence_number','namuna_code','client_category_detail','is_back','back_remarks','submit_back_remarks']

    def get_client_category_detail(self,obj):
        return obj.client_category_detail.client_category_id

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['status'] = over_all_status[instance.status]
        representation['assigned_date'] = instance.supervisor_sample_form.first().created_date
        
        return representation