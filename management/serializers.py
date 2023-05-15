from .models import ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment
from rest_framework import serializers

class SampleFormHasParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 
    
    def validate(self, attrs):
        sample_form = attrs.get('sample_form')
        analyst_user = attrs.get('analyst_user')
        parameter = attrs.get('parameter')

        action = self.context['view'].action

        print("vlidation...")
        print(analyst_user)
        # Check uniqueness of analyst_user for the sample_form
        # if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists():
        #     raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst_user already exists.')

        # # Check uniqueness of parameter for the sample_form
        # for param in parameter:
        #     if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
        #         raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists.')

        return attrs


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategory
        fields = '__all__'        

class PaymentSerializer(serializers.ModelSerializer):
        class Meta:
            model = Payment
            fields = '__all__' 

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class SampleFormSerializer(serializers.ModelSerializer):
    parameters = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = SampleForm
        fields = '__all__'

class CommoditySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
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
    
    commodity = CommoditySerializer(many=True,read_only=True)
    class Meta:
        model = CommodityCategory
        fields = '__all__'
