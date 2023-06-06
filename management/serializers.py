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
            # Check if the parameter exists in SampleFormHasParameter model
            exists = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id).exists()
            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation

class SampleFormWriteSerializer(serializers.ModelSerializer):
    # def validate(self, data):
    #     parameters = data.get('parameters')
           
    #     #id = data.get('id')
    #     if len(parameters) == 0:
    #         commodity = data.get('commodity')   
    #         parameters = TestResult.objects.filter(commodity=commodity)
    #         data['parameters'] = parameters
    #     return data
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
        is_tested = True
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            # formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(commodity=obj.commodity_id,parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            # print(obj.commodity_id)
            # print(parameter['id'])
            parameter['result'] = formula_calculate.result if formula_calculate else "-"
            
            if formula_calculate == None:
                is_tested = False
            
        return parameter_data,is_tested
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        parameter,is_tested = self.get_parameter(instance)
        representation['parameter'] = parameter
        representation['is_tested'] = is_tested

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
        print(action)

        if len(attrs) == 1 and action == 'partial_update' and 'status' in attrs:
            return attrs
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')

        print("vlidation...")
        print(analyst_user)
    
        print("SAdd")
        if action == "create":
            if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists():
                raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst already exists(create)')
            
            for param in parameter:
                # print(param)
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    # obj = SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param)
                    print("creating")
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(create)')
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
            print(str(instance_id)+" instanse id")
            sample_form_has_parameter_obj = SampleFormHasParameter.objects.get(id=instance_id)  

            if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                print("trying to update with same parameter")

            else:
                raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst already exists(update)')
            
            for param in parameter:
                # print(param)
                if sample_form_has_parameter_obj.parameter.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    print("trying to update with same parameter")
                    pass
                elif SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(update)')
                   

        return attrs
