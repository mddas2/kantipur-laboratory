from rest_framework import serializers
from account import roles

from rest_framework import serializers
from .. encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from ..models import Commodity,SampleForm,SampleFormHaveInspector
from account.models import CustomUser

class CustomUserInspectorSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUserInspectorSerializer"
        model = CustomUser
        fields = ['first_name','last_name','id']

class SampleFormHaveInspector_SampleFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHaveInspector
        fields = '__all__'


class CommoditySampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = ['name','id']

class SampleFormInspectorListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    commodity = CommoditySampleFormSerializer(read_only = True,many=False)
    inspector = SampleFormHaveInspector_SampleFormSerializers(read_only = True)
    owner_user_obj = CustomUserInspectorSerializer(read_only = True)
    class Meta:
        model = SampleForm
        fields = ['id','name','new_name','commodity','refrence_number','sample_lab_id','status','namuna_code','created_date','inspector','owner_user_obj']


    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed" or status == "recheck":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"
        return representation
    