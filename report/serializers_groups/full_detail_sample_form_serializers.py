from ..utilities.base_import import *
from management.status_naming import over_all_status
from management.models import ClientCategoryDetail,SuperVisorSampleForm,Commodity,SampleFormHasParameter,SampleForm,TestResult,Payment
from account.models import CustomUser
from management.encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from report.analyst_standard_result import getStandardResult

class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    # ClientCategoryDetail = ClientCategoryDetailImagesSerializer(many=True,read_only=True)
    class Meta:
        ref_name = "ClientCategoryDetailSerializer"
        model = ClientCategoryDetail
        fields = '__all__'

class CustomUserSuperVisorUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_report_finalserializer"
        model = CustomUser
        fields = ['first_name','last_name'] 

class SupervisorSampleFormSerializer(serializers.ModelSerializer):
    supervisor_user = CustomUserSuperVisorUserSerializer(read_only = True)
    class Meta:
        ref_name = "SupervisorSampleFormSerializer"
        model = SuperVisorSampleForm
        fields = ['supervisor_user']

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_report_finalserializer"
        model = Commodity
        fields = ['name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUser_report_finalserializer"
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        ref_name = "SampleFormHasParameter_final_report"
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date'] 

class TestResultLimitedSerializer(serializers.ModelSerializer):
     class Meta:
        model = TestResult
        ref_name = "TestResultLimitedSerializer"
        exclude = ['units', 'mandatory_standard', 'test_method']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "report_payment_detail"
        model = Payment
        fields = '__all__'
        depth = 1

class DetailFullSampleFormSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    parameters = TestResultLimitedSerializer(read_only = True, many = True)
    # verified_by = CustomUserSerializer(read_only = True)
    # approved_by = CustomUserSerializer(read_only = True)

    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only = True)

    payment = PaymentSerializer(read_only = True,many = True)

    id = serializers.SerializerMethodField()

    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    
    class Meta:
        model = SampleForm
        fields = fields = ['id','name','new_name','commodity','refrence_number','sample_lab_id','client_category_detail','status','namuna_code','created_date','owner_user_obj','payment','parameters','mfd','dfb','days_dfb','dfb_duration','dfb_type','batch','brand','purpose','condition','note','amendments','sample_type','sample_units','sample_quantity','number_of_sample','analysis_fee','voucher_number','voucher_date','price','supervisor_sample_form']


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        sample_form_id = representation.get('id')
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,self.context['request'].user)
        # Add extra response data for parameters field
        parameters_data = representation.get('parameters', [])
        user = self.context['request'].user
        if user.role == roles.SMU or user.role == roles.SUPERADMIN:
            smu_superadmin_status = representation.get('status')
            representation['status'] = over_all_status[smu_superadmin_status]
        

        for parameter_data in parameters_data:
            parameter_id = parameter_data.get('id')
            # Check if the parameter exists in SampleFormHasParameter model
            # print(parameter_id)
            if user.role == roles.SMU or user.role == roles.SUPERADMIN or user.role == roles.VERIFIER or user.role == roles.ADMIN:
                sample_form_has_supervisor_obj = instance.supervisor_sample_form.all().filter(parameters = parameter_id)
                exists_sup = sample_form_has_supervisor_obj.exists()
                if exists_sup:
                    sup_full_name = str(sample_form_has_supervisor_obj.first().supervisor_user.first_name) +' '+ str(sample_form_has_supervisor_obj.first().supervisor_user.last_name)
                    parameter_data['sup_full_name'] = sup_full_name

            sample_form_has_assigned_analyst_obj = instance.sample_has_parameter_analyst.all().filter(parameter=parameter_id)
            exists = sample_form_has_assigned_analyst_obj.exists()
            
            if exists:
                analyst_obj = sample_form_has_assigned_analyst_obj.first().analyst_user
                first_name = analyst_obj.first_name
                last_name = analyst_obj.last_name
                created_date = sample_form_has_assigned_analyst_obj.first().created_date
                parameter_data['first_name'] = first_name
                parameter_data['last_name'] = last_name
                
                parameter_data['sample_form_has_parameter'] = sample_form_has_assigned_analyst_obj.first().id  
                parameter_data['assigned_date'] = created_date
                
                formula_obj_result = instance.result.all().filter(parameter_id = parameter_id)
                if formula_obj_result.count()>0:
                    parameter_data['status'] = formula_obj_result.first().status

                    parameter_data['result'] = getStandardResult(formula_obj_result)

                    parameter_data['units'] = formula_obj_result.first().units
                    parameter_data['mandatory_standard'] = formula_obj_result.first().mandatory_standard
                    parameter_data['test_method'] = formula_obj_result.first().test_method

                else:
                    parameter_data['status'] = "processing"
                    parameter_data['result'] = '-'
            else:
                parameter_data['status'] = "not_assigned"

        representation['parameters'] = parameters_data

        try:
            representation['analysis_completed_date'] = instance.sample_has_parameter_analyst.all().order_by('-completed_date').first().completed_date
        except:
            representation['analysis_completed_date'] = ''
        
        try:
            representation['analysis_started_date'] = instance.sample_has_parameter_analyst.all().order_by('id').first().started_date
        except:
            representation['analysis_started_date'] = '-'
        
        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name
        representation['client_category'] = client_category_detail

        return representation