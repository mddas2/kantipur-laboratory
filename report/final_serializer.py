from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter,SuperVisorSampleForm
from account.models import CustomUser
from rest_framework import serializers
from management import roles
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from management.status_naming import over_all_status

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_report_finalserializer"
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_report_finalserializer"
        model = Commodity
        fields = ['name']

class SupervisorSampleFormSerializer(serializers.ModelSerializer):
    supervisor_user = CustomUserSerializer(read_only = True)
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

class CompletedSampleFormHasVerifierSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_user = CustomUserSerializer(read_only=True)
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    class Meta:
        name = "CompletedSampleFormHasVerifierSerializer_report_"
        model = SampleForm
        fields = ['id','name','supervisor_user','sample_has_parameter_analyst','commodity','status','created_date','completed_date'] #user access

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
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only=True)
    
    class Meta:
        name = "AssignedSampleForSmuSuperAdminSerializer"
        model = SampleForm
        fields = ['id','supervisor_sample_form','name','sample_has_parameter_analyst','commodity','status','created_date','refrence_number','sample_lab_id']

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')


        representation['status'] = over_all_status[instance.status]
            
        
        return representation