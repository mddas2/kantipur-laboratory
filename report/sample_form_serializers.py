from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter,SuperVisorSampleForm
from account.models import CustomUser
from rest_framework import serializers
from management.status_naming import over_all_status
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_reportsample_form"
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_reportsample_form"
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "SampleFormHasParameter_reportsample_form"
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date','status'] 

class SampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "SupervisorSampleform"
        model = SampleForm
        fields = '__all__'
    
    def to_representation(self, instance): #if dftqc then sample name as commodity category else do no things
        representation = super().to_representation(instance)
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            #representation['name'] = instance.commodity.name #"error md fix" #sample_name
            if instance.new_name != None:
                representation['name'] = instance.new_name#instance.new_names
        representation['client_category'] = client_category_detail
        return representation

class SampleFormHasSupervisorParameter_SampleFormSerializer(serializers.ModelSerializer): #SampleFormHasSupervisorParameterSerializer
    commodity = CommoditySerializer(read_only = True)
    class Meta:
        ref_name = "SampleFormHasSupervisorParameter_SampleFormSerializer"
        model = SampleForm
        fields = ['name','client_category_detail','namuna_code','commodity']
    
    # def to_representation(self, instance): #if dftqc then sample name as commodity category else do no things
    #     representation = super().to_representation(instance)
    #     client_category_detail = instance.client_category_detail.client_category.id
    #     if client_category_detail == 11:
    #         representation['name'] = instance.commodity.name #"error md fix" #sample_name
    #     representation['client_category'] = client_category_detail
    #     return representation


class SampleFormHasSupervisorParameterSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True) 
    sample_form = SampleFormHasSupervisorParameter_SampleFormSerializer(read_only = True)
 
    class Meta:
        model = SuperVisorSampleForm
        fields = ['id','sample_form','sample_has_parameter_analyst','status','created_date','is_analyst_test']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation['status'] = over_all_status[instance.status]
        return representation
                