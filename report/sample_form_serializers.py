from management.models import SampleForm, Commodity,SampleFormHasParameter
from rest_framework import serializers
from management import roles

from management.models import SampleForm, Commodity,SampleFormHasParameter
from account.models import CustomUser
from rest_framework import serializers

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','id'] 

class CommoditySerializer(serializers.ModelSerializer):
    class Meta:
        model = Commodity
        fields = ['name']

class SampleFormHasParameterReadSerializer(serializers.ModelSerializer):
    analyst_user = CustomUserSerializer(read_only = True)
    class Meta:
        model = SampleFormHasParameter
        fields = ['analyst_user','created_date','status'] 

class SampleFormHasAnalystSerializer(serializers.ModelSerializer):
    sample_has_parameter_analyst = SampleFormHasParameterReadSerializer(many=True,read_only=True)
    commodity = CommoditySerializer(read_only = True)
    class Meta:
        model = SampleForm
        fields = ['id','name','sample_has_parameter_analyst','commodity','status','created_date']

    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
    
        request = self.context.get('request')
      
        if request.user.role == roles.SUPERVISOR:
            is_analyst_test = representation.get('is_analyst_test')
            if is_analyst_test == True:
                stat = "completed"
                representation['status'] = stat
        return representation
                