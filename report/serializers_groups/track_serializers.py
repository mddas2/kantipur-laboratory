from ..utilities.base_import import *
from management.status_naming import over_all_status
from management.models import ClientCategoryDetail,SuperVisorSampleForm,Commodity,SampleFormHasParameter,SampleForm
from account.models import CustomUser
from management.encode_decode import generateAutoEncodeIdforSampleForm

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

class TrackSampleFormSerializer(serializers.ModelSerializer):
    commodity = CommoditySerializer(read_only = True)
    supervisor_sample_form = SupervisorSampleFormSerializer(many = True,read_only = True)
    id = serializers.SerializerMethodField()
    
    def get_id(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    class Meta:
        name = "TrackSampleFormSerializer"
        model = SampleForm
        fields = ['id','supervisor_sample_form','name','commodity','status','created_date','completed_date','namuna_code'] #user access


    def to_representation(self, instance):
        representation = super().to_representation(instance)

        request = self.context.get('request')

        client_category_detail = instance.client_category_detail.client_category.id
        if client_category_detail == 11:
            representation['name'] = instance.commodity.name #"error md fix" #sample_name

        status = representation.get('status')
        if request.user.role == roles.SUPERVISOR:
            
            if status == "completed":
                stat = "verified"
                representation['status'] = stat
            else:
                representation['status'] = over_all_status[status]
        else:
            representation['status'] = over_all_status[status]

        return representation