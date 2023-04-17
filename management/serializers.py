from .models import ClientCategory, SampleForm, Commodity, CommodityCategory
from rest_framework import serializers


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'
        

class SampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = '__all__'
        
        
class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = '__all__'
        
        
class CommodityCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CommodityCategory
        fields = '__all__'