from .models import SampleFormVerifier,SampleForm
from rest_framework import serializers
from . encode_decode import generateDecodeIdforSampleForm,generateAutoEncodeIdforSampleForm

class SampleFormWriteVerifierSerilizer(serializers.ModelSerializer):
 
    def validate(self, data):
        
        if data.get('sample_form') !=None :
            sample_form_id = data.get('sample_form').id
            sample_form_obj = SampleForm.objects.get(id=sample_form_id)
            print("Asd dsa ")
            if sample_form_obj.is_analyst_test == False:
                raise serializers.ValidationError("Analyst have not sent sample test to supervisor.")
        
        action = self.context['view'].action
        if action == 'partial_update' or action == "update":
            is_verified = data.get('is_verified')

            if is_verified ==  True: 
                instance = self.instance
                sample_form_obj = instance.sample_form                
                request = self.context.get('request')
                sample_form_obj.verified_by = request.user                
                sample_form_obj.save()

        
        return data
    
    sample_form = serializers.SerializerMethodField()

    def get_sample_form(self, obj):
        user = self.context['request'].user
        return generateAutoEncodeIdforSampleForm(obj.id,user)
    
    class Meta:
        model = SampleFormVerifier
        fields = '__all__'
    


 