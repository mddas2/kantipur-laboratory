from .models import MicroObservationTableRawData,MicroParameterRawData,RawDataSheet,SampleForm,RawDataSheetDetail,TestResult,MicroParameter,MicroObservationTable,SampleFormHasParameter
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

class MicroObservationSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "management.raw_data_serializer.MicroObservationSerializer"
        model = MicroObservationTable
        fields = '__all__'

class MicroTableSerializer(serializers.ModelSerializer):
    micro_observation_table = MicroObservationSerializer(read_only = True,many=True)
    class Meta:
        ref_name = "management.raw_data_serializer.micro_table"
        model = MicroParameter
        fields = '__all__'

class MicroObservationRawDataSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "management.raw_data_serializer.MicroObservationSerializer"
        model = MicroObservationTableRawData
        fields = '__all__'

class MicroTableRawDataSerializer(serializers.ModelSerializer):
    micro_observation_table_raw_data = MicroObservationRawDataSerializer(read_only = True,many=True)
    class Meta:
        ref_name = "management.raw_data_serializer.micro_table"
        model = MicroParameterRawData
        fields = '__all__'

class rawDataSheetDetailSerializer(serializers.ModelSerializer):
    parameter = TestResultSerializer(read_only = True)
    micro_table = MicroTableRawDataSerializer(read_only = True) 
    class Meta:
        model = RawDataSheetDetail
        fields = '__all__'

class SampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['id', 'name','created_date','remarks']

class SampleFormHasParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = ['created_date']

class rawDataSerializer(serializers.ModelSerializer):

    # def get_sample_form(self, obj):
    #     user = self.context['request'].user
    #     return generateAutoEncodeIdforSampleForm(obj.id,user)
    raw_data = rawDataSheetDetailSerializer(read_only = True,many=True)
    analyst_user = ApprovedBySerializer(read_only = True,many=False)
    sample_form_has_parameter = SampleFormHasParameterSerializer(read_only = True)
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
        # try:
        #     representation['status'] = over_all_status[instance.status]
        # except:
        #     representation['status'] = "completed" # blunder need to fix
        return representation
  

class rawDataTestTypeGlobalSerializer(serializers.ModelSerializer):

    raw_data = rawDataSheetDetailSerializer(read_only = True,many=True)
    analyst_user = ApprovedBySerializer(read_only = True,many=False)
    supervisor_by = serializers.SerializerMethodField()
    # sample_form = SampleFormSerializer(read_only=True, many=True)
    class Meta:
        model = RawDataSheet
        fields = '__all__'
    
        
    def get_supervisor_by(self, obj):
        supervisor_table_obj = obj.super_visor_sample_form
        try:
            user = CustomUser.objects.get(id=supervisor_table_obj.supervisor_user.id)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None
        

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        representation['sample_form'] = SampleFormSerializer(instance.sample_form).data
        representation['status'] = over_all_status[instance.status]
        return representation