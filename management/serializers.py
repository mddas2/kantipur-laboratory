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
    def validate_name(self,value):#field level validation
        if value == "test":
            raise serializers.ValidationError('name test should not be there error')
        return value
    
    def validate(self, data):
        name = data.get('name')
        #id = data.get('id')
        if name == "test":
            raise serializers.ValidationError('name test should not be there error')
        return data

    class Meta:
        model = CommodityCategory
        fields = '__all__'

   