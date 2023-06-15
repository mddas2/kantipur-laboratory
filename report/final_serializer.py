from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter
from account.models import CustomUser
from rest_framework import serializers

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
    class Meta:
        model = SampleForm
        fields = ['id','name','supervisor_user','sample_has_parameter_analyst','commodity','status','created_date']