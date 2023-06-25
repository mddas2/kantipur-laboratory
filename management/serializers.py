from .models import ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate
from rest_framework import serializers
from account.models import CustomUser
from . import roles
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from . raw_data import generateRawData

class ApprovedBySerializer(serializers.ModelSerializer):
     class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','id'] 

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

class CommoditySerializer(serializers.ModelSerializer):
    test_result = TestResultSerializer(many=True,read_only=True)
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = '__all__'

# class CommoditySerializer(serializers.ModelSerializer):
#     class Meta:
#         ref_name = "Commodity_sample_form"
#         model = Commodity
#         fields = '__all__


class SampleFormReadSerializer(serializers.ModelSerializer):

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    parameters = TestResultSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    owner_user = serializers.SerializerMethodField()
    approved_by = ApprovedBySerializer(read_only = True,many=False)
    verified_by = ApprovedBySerializer(read_only = True,many=False)
    supervisor_user = ApprovedBySerializer(read_only = True)

    commodity = CommoditySerializer(read_only = True,many=False)
    
    class Meta:
        approved_by = ApprovedBySerializer(read_only = True)
        supervisor_user = ApprovedBySerializer(read_only = True)
        verified_by = ApprovedBySerializer(read_only = True)
        model = SampleForm
        fields = '__all__'

    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        parameters_data = representation.get('parameters', [])

        assigned = 0
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            smple_frm_exist = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = smple_frm_exist.exists()
            parameter_data['exist'] = exists
            
            if exists:
                # print(smple_frm_exist.first().analyst_user.username)
                try:
                    parameter_data['status'] = "assigned"
                    parameter_data['analyst'] = smple_frm_exist.first().analyst_user.username
                except:
                    pass           


            if exists == True:
                assigned+=1

        representation['total_assign'] = assigned
        representation['parameters'] = parameters_data
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"


        return representation

class SampleFormWriteSerializer(serializers.ModelSerializer):
    def validate(self, data):
        action = self.context['view'].action
        if action == "create":
            parameters = data.get('parameters')
            
            #id = data.get('id')
            if len(parameters) == 0:
                commodity = data.get('commodity')   
                parameters = TestResult.objects.filter(commodity=commodity)
                data['parameters'] = parameters
            return data
        elif action == "partial_update" or action == "update":
            supervisor_user = data.get('supervisor_user')
            form_available = data.get('form_available')
       
            if supervisor_user is not None and form_available == "supervisor":
                request = self.context.get('request')
                data['approved_by'] = request.user
            return data
        else:
            return data
        
    class Meta:
        model = SampleForm
        fields = '__all__'

class SampleFormReadAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only=True,many=False)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = ApprovedBySerializer(read_only = True)

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    def validate(self, data):
        action = self.context['view'].action
        if action == "create":
            parameters = data.get('parameters')
            
            #id = data.get('id')
            if len(parameters) == 0:
                commodity = data.get('commodity')   
                parameters = TestResult.objects.filter(commodity=commodity)
                data['parameters'] = parameters
            return data
        else:
            return data
        
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return ApprovedBySerializer(user).data
        except CustomUser.DoesNotExist:
            return None

    class Meta:
        
        model = SampleForm
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
    sample_form = SampleFormReadAnalystSerializer(read_only=True)
    commodity = CommodityWriteSerializer(read_only=True,many=True)
    parameter = TestResultSerializer(many=True,read_only=True)
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 


    def get_parameter(self, obj):
        parameter_data = TestResultSerializer(obj.parameter, many=True).data
  
        count_status = 0
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id).first()
            if formula_calculate:
                parameter['result'] = formula_calculate.result               
                count_status = count_status + 1   
            else:
                parameter['result'] = ""      
         
        analyst_status = "processing"
        completed_done = 0
        for parameter in parameter_data:
            formula_calculate = SampleFormParameterFormulaCalculate.objects.filter(parameter = parameter['id'],sample_form=obj.sample_form_id)
            if formula_calculate.exists():
                if formula_calculate.first().result != None:                
                    analyst_status = "completed"   
                    completed_done = completed_done + 1
                else:
                    analyst_status = "tested"
                    break
            else:                
                analyst_status = "processing" 
                break     
                
        total_len = len(parameter_data)
        print(completed_done,"md",total_len)
        if completed_done == 0:
            completed_done = str(total_len)
        elif completed_done == total_len:
            completed_done = ''
            print(analyst_status)
        else:
            completed_done = str(total_len)+"/"+str(completed_done)
        

        if count_status == 0:
            analyst_status = "pending"       
       
            
        return parameter_data,analyst_status,completed_done
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.parameter.first().id)
        parameter,analyst_status,total_completed = self.get_parameter(instance)
        representation['parameter'] = parameter

        representation['status'] = analyst_status
        representation['completed_done'] = total_completed

        return representation

class SampleFormHasParameterWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__' 

    def to_internal_value(self, data):
        if 'sample_form' in data:
            sample_form_id = data['sample_form'] 
            decoded_sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)#smart_text(urlsafe_base64_decode(data['sample_form']))
            data['sample_form'] = decoded_sample_form_id
            print(data['sample_form'])
        return super().to_internal_value(data)
    
    def validate(self, attrs):
        sample_form = attrs.get('sample_form')
        print(sample_form," not  printing this...")
        analyst_user = attrs.get('analyst_user')
        parameter = attrs.get('parameter')

        action = self.context['view'].action
    
        if len(attrs) == 3 and action == 'partial_update' and 'is_supervisor_sent' and 'status' and 'remarks' in attrs:
            if attrs.get('is_supervisor_sent') == True:
                id=self.context['view'].kwargs.get('pk')
                generateRawData(id) #  if sent to supervisor then generate logs
                return attrs
        elif action == 'partial_update':
            raise serializers.ValidationError('Partial updates not allowed....')
  
        if action == "create":
            for param in parameter:
                # print(param)
                if SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists():
                    # obj = SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param)     
                    print("error")        
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(create)')
            
          
        elif action == 'update' or action == 'partial_update':            
            instance_id = self.instance.id 
           
            sample_form_has_parameter_obj = SampleFormHasParameter.objects.get(id=instance_id)  

            if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists() and sample_form_has_parameter_obj.sample_form == sample_form:
                pass

            else:
                raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and analyst already exists(update)')
            
            for param in parameter:
                if sample_form_has_parameter_obj.parameter.filter(id=param.id).exists() and sample_form_has_parameter_obj.sample_form == sample_form: #if try to update same parameter as previous stored then dod nothing
                    pass
                elif SampleFormHasParameter.objects.filter(sample_form=sample_form, parameter=param).exists(): #if try to update and not same as previous parameter then check already exist parameter.if exist then raise error
                    raise serializers.ValidationError('A SampleFormHasParameter with the same sample_form and parameter already exists(update)')
                   

        return attrs
    
    def create(self, validated_data):
        sample_form = validated_data['sample_form']
        analyst_user = validated_data['analyst_user']
        parameter = validated_data['parameter']

        if SampleFormHasParameter.objects.filter(sample_form=sample_form, analyst_user=analyst_user).exists():
            print("testing ok append parameter")
            instance = SampleFormHasParameter.objects.get(sample_form=sample_form, analyst_user=analyst_user)
            # Append the new parameters to the existing instance
            instance.parameter.add(*parameter)
            return instance
        
        return super().create(validated_data)
