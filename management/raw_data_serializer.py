from .models import RawDataSheet,SampleForm,RawDataSheetDetail,TestResult
from account.models import CustomUser
from rest_framework import serializers
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from .status_naming import over_all_status

class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        ref_name = "jpts"
        model = CustomUser
        fields = ['first_name','last_name','email','id'] 

class TestResultSerializer(serializers.ModelSerializer):
    
    class Meta:
        ref_name = "management.raw_data_serializer.TestResultSerializers"
        model = TestResult
        fields = '__all__'

class rawDataSheetDetailSerializer(serializers.ModelSerializer):
    parameter = TestResultSerializer(read_only = True)
    class Meta:
        model = RawDataSheetDetail
        fields = '__all__'

class SampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['id', 'name','created_date','remarks']

class rawDataSerializer(serializers.ModelSerializer):

    # def get_sample_form(self, obj):
    #     user = self.context['request'].user
    #     return generateAutoEncodeIdforSampleForm(obj.id,user)
    raw_data = rawDataSheetDetailSerializer(read_only = True,many=True)
    analyst_user = ApprovedBySerializer(read_only = True,many=False)
    # sample_form = SampleFormSerializer(read_only=True, many=True)
    class Meta:
        model = RawDataSheet
        fields = '__all__'

    def to_representation(self, instance):
        # print(instance.super_visor_sample_form)
        representation = super().to_representation(instance)
        representation['sample_form'] = SampleFormSerializer(instance.sample_form).data
        representation['status'] = over_all_status[instance.status]
        return representation

class rawDataTestTypeSerializer(serializers.ModelSerializer):

    # def get_sample_form(self, obj):
    #     user = self.context['request'].user
    #     return generateAutoEncodeIdforSampleForm(obj.id,user)
    raw_data = rawDataSheetDetailSerializer(read_only = True,many=True)
    analyst_user = ApprovedBySerializer(read_only = True,many=False)
    # sample_form = SampleFormSerializer(read_only=True, many=True)
    class Meta:
        model = RawDataSheet
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['sample_form'] = SampleFormSerializer(instance.sample_form).data
        representation['status'] = over_all_status[instance.status]
        return representation

 