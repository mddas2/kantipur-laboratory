from rest_framework  import serializers
from ..models import SampleForm
from account import roles

class IsBackSampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['name','condition','mfd','dfb','days_dfb','dfb_duration','dfb_type','batch','brand','purpose','requested_export','report_date','amendments']

class IsBackSubmitSampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['is_back','submit_back_remarks','is_back_submit']

    def validate_is_back(self,value):
        request = self.context.get('request')
        if request.user.role in [roles.SMU,roles.SUPERVISOR,roles.VERIFIER]:
            return ''
        raise serializers.ValidationError('You have not permission to set is_back.')
    
    def validate_is_back_submit(self,value):
        request = self.context.get('request')
        if request.user.role in [roles.SMU,roles.SUPERVISOR,roles.VERIFIER]:
           
            return value    
        raise serializers.ValidationError('You have not permission to set is_back_submit.')
    
    def validate_submit_back_remarks(self,value):
        request = self.context.get('request')
        if request.user.role in [roles.SMU,roles.SUPERVISOR,roles.VERIFIER]:
            return value
        else:
            raise serializers.ValidationError('You have not permission to set back remarks.')
