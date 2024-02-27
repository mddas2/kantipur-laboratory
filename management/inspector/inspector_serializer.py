from rest_framework import serializers
from account import roles

from rest_framework import serializers
from .. encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm
from ..models import Commodity,SampleForm,SampleFormHaveInspector,TestResult,SuperVisorSampleForm
from account.models import CustomUser

class TestResultLimitedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        exclude = ['units', 'mandatory_standard', 'test_method','formula','price','commodity']

class CustomUserInspectorSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "CustomUserInspectorSerializer"
        model = CustomUser
        fields = ['first_name','last_name','id']

class SampleFormHaveInspector_SampleFormSerializers(serializers.ModelSerializer):
    class Meta:
        model = SampleFormHaveInspector
        fields = '__all__'


class CommoditySampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "Commodity_management"
        model = Commodity
        fields = ['name','id']

class SampleFormInspectorListSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    commodity = CommoditySampleFormSerializer(read_only = True,many=False)
    inspector = SampleFormHaveInspector_SampleFormSerializers(read_only = True)

    class Meta:
        model = SampleForm
        fields = ['id','name','new_name','commodity','refrence_number','sample_lab_id','status','namuna_code','created_date','inspector']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed" or status == "recheck":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"
        return representation
    

class SampleFormInspectorRetrieveSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)

    commodity = CommoditySampleFormSerializer(read_only = True,many=False)
    inspector = SampleFormHaveInspector_SampleFormSerializers(read_only = True)
    # owner_user_obj = CustomUserInspectorSerializer(read_only = True)
    parameters = TestResultLimitedSerializer(many = True,read_only = True)
    class Meta:
        model = SampleForm
        fields = ['id','name','new_name','commodity','refrence_number','sample_lab_id','status','namuna_code','created_date','inspector','parameters','owner_user_obj','price']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        status = representation.get('status')
        request = self.context.get('request')

        if request.user.role == roles.USER:
            if status == "pending" or status == "processing" or status=="completed" or status == "recheck":
                representation['status'] = status
            else:
                representation['status'] = "processing"
                
        if request.user.role == roles.SUPERVISOR:
            if status == "not_assigned":
                representation['status'] = "Not Assigned"
        return representation
    

class SampleFormWriteSerializer_Inspector(serializers.ModelSerializer):

    def validate(self, data):
        # raise serializers.ValidationError('testing sample form dftqc')
        parameters = data.get('parameters')
        request = self.context.get('request')

        if parameters and (request.user.role != roles.SMU and request.user.role != roles.INSPECTOR):
            raise serializers.ValidationError('You have not permission to update parameters. Error code E-SAMPLE-FORM-1')
        
        sample_form_id = self.instance.id
        supervisor_data = SuperVisorSampleForm.objects.filter(sample_form_id = sample_form_id).exists()
        if supervisor_data and parameters: #if sampleform  reach to supervisor , then no one can update parameters.
            raise serializers.ValidationError('You have not permission to update parameters as sample is forwarded to lab. Error code E-SAMPLE-FORM-4')
      
        if request.user.role == roles.ADMIN:
            if len(data) == 2 and 'status' in data and 'admin_remarks' in data:
                request = self.context.get('request')
                approved_by = CustomUser.objects.all().filter(id = int(request.data.get('approve_by')))
                if approved_by.exists() == False:
                    raise serializers.ValidationError("Verified by user must be exists")    
                data['approved_by_id'] = approved_by.first().id
                return data
            else:
                raise serializers.ValidationError('You have not permission. Error code E-SAMPLE-FORM-2')
        elif request.user.role == roles.VERIFIER:
            return data #blunder md blunder_md  hints more validate
        elif request.user.role == roles.SUPERVISOR:
            return data #blunder md blunder_md  hints more validate
        elif request.user.role == roles.SMU or request.user.role == roles.INSPECTOR:
            commodity = data.get('commodity')
            commodity_parameters = TestResult.objects.filter(commodity=commodity)
            commodity_price = Commodity.objects.get(id = commodity.id).price
        
            if len(parameters) == 0:  
                data['parameters'] = commodity_parameters
            
            if data.get('analysis_pricing') == False:      
                data['price'] = commodity_price
            else:
                price = 0
                for paramet in data.get('parameters'):
                    price = paramet.price + price
                data['price'] = price
            return data
        
        else:
            raise serializers.ValidationError('You have not permission.Error code E-SAMPLE-FORM-3 ')
        #for verifier validate.
        
    class Meta:
        model = SampleForm
        fields = '__all__'

    def get_fields(self):
        fields = super(SampleFormWriteSerializer_Inspector, self).get_fields()
        # Check if the request method is PUT or PATCH
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            fields['owner_user_obj'].read_only = True
            fields['price'].read_only = True

        return fields
    