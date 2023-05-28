from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers


class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only=True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','commodity'] 

class SampleFormHasAnalystSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    class Meta:
        model = SampleForm
        fields = ['name','sample_has_parameter_analyst']
