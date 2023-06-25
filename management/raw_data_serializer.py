from .models import RawDataSheet,SampleForm,RawDataSheetDetail
from rest_framework import serializers
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm


class rawDataSheetDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RawDataSheetDetail
        fields = '__all__'

class rawDataSerializer(serializers.ModelSerializer):

    # def get_sample_form(self, obj):
    #     user = self.context['request'].user
    #     return generateAutoEncodeIdforSampleForm(obj.id,user)
    raw_data = rawDataSheetDetailSerializer(read_only = True,many=True)
    class Meta:
        model = RawDataSheet
        fields = '__all__'
    


 