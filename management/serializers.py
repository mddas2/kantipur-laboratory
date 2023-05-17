from .models import ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate
from rest_framework import serializers

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


class SampleFormReadSerializer(serializers.ModelSerializer):
    parameters = TestResultSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = SampleForm
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])
      
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            print(parameter_id)

            # Check if the parameter exists in SampleFormHasParameter model
            exists = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id).exists()
            print(exists)
            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation

class SampleFormWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = '__all__'


class CommoditySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = Commodity
        fields = '__all__'

class CommodityWriteSerializer(serializers.ModelSerializer):
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

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    sample_form = SampleFormWriteSerializer(read_only=True)
    commodity = CommodityWriteSerializer(read_only=True)
    parameter = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 


    def get_parameter(self, obj):
        parameter_data = TestResultSerializer(obj.parameter, many=True).data

        # Extract the parameter identifiers from obj.parameter
        # parameter_ids = [parameter['id'] for parameter in parameter_data]
        # print(parameter_ids)

        # Filter SampleFormParameterFormulaCalculate by commodity_id, parameter_ids, and sample_form_id
     
        # print(obj.parameter)
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(commodity_id=obj.commodity_id,parameter_id = parameter['id'],sample_form_id=obj.sample_form_id).first()
            parameter['result'] = formula_calculate.result if formula_calculate else "10"
        return parameter_data
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        representation['parameter'] = self.get_parameter(instance)
        return representation

class SampleFormHasParameterWriteSerializer(serializers.ModelSerializer):
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
