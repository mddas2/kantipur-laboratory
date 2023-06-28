from management.models import SampleForm, Commodity,SampleFormHasParameter,TestResult,SampleFormParameterFormulaCalculate,Payment
from rest_framework import serializers

from management.models import SampleForm, Commodity,SampleFormHasParameter
from account.models import CustomUser
from rest_framework import serializers
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

from management import roles

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','id','email'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "report_payment_detail"
        model = Payment
        fields = '__all__'

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class ParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class DetailSampleFormHasParameterAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = ParameterSerializer(read_only = True, many = True)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = CustomUserSerializer(read_only = True)
    verified_by = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        request = self.context.get('request')
        user = request.user
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        normal_status = representation.get('status')
        if normal_status == "not_assigned":
            representation['status'] = "Processing"

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])

        params_data_fixed = []
        for param in parameters_data:
            parameter_id = param.get('id')
            obk = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id,analyst_user=user)
            exists = obk.exists()
            if exists:
                params_data_fixed.append(param)    

        parameters_data = params_data_fixed
      
        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
           
            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id,analyst_user=user)
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'
            else:
                parameters_data.remove(parameter_data) 

            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation
    

class DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = ParameterSerializer(read_only = True, many = True)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = CustomUserSerializer(read_only = True)
    verified_by = CustomUserSerializer(read_only = True)
    
    
    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])

        user = self.context['request'].user

        if user.role == roles.SMU or user.role == roles.SUPERADMIN:
            smu_superadmin_status = representation.get('status')
            if smu_superadmin_status == "not_assigned" or smu_superadmin_status == "not_verified":
                representation['status'] = "processing"

        elif user.role == roles.USER:
            representation['payment'] = PaymentSerializer(instance.payment).data

        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            # print(parameter_id)
            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['sample_form_has_parameter'] = sample_form_has_assigned_analyst_obj.first().id
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'


            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation


class FinalReportNepaliAnalystSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = ParameterSerializer(read_only = True, many = True)
    owner_user = serializers.SerializerMethodField()
    supervisor_user = CustomUserSerializer(read_only = True)
    verified_by = CustomUserSerializer(read_only = True)
    
    
    class Meta:
        model = SampleForm
        fields = '__all__'
    
    def get_owner_user(self, obj):
        email = obj.owner_user
        try:
            user = CustomUser.objects.get(email=email)
            return CustomUserSerializer(user).data
        except CustomUser.DoesNotExist:
            return None


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')

        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])

        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            # print(parameter_id)
            sample_form_has_assigned_analyst_obj = SampleFormHasParameter.objects.filter(parameter=parameter_id, sample_form = sample_form_id)
            exists = sample_form_has_assigned_analyst_obj.exists()
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                status = sample_form_has_assigned_analyst_obj.first().status
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                parameter_data['sample_form_has_parameter'] = sample_form_has_assigned_analyst_obj.first().id
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id,parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status
                    parameter_data['result'] = formula_obj_result.first().result
                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'


            parameter_data['exist'] = exists

        representation['parameters'] = parameters_data
        return representation