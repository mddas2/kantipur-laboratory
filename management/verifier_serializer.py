from .models import SampleFormVerifier,SampleForm
from rest_framework import serializers

class SampleFormWriteVerifierSerilizer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormVerifier
        fields = '__all__'

    def validate(self, data):
        if data.get('sample_form') !=None :
            sample_form_id = data.get('sample_form').id
            sample_form_obj = SampleForm.objects.get(id=sample_form_id)

            is_verified = data.get('is_verified')

            if is_verified is not None and is_verified ==  True:
                request = self.context.get('request')
                sample_form_obj.verified_by = request.user
                sample_form_obj.save()

            if sample_form_obj.is_analyst_test == False:
                raise serializers.ValidationError("Analyst have not sent sample test to supervisor.")

        return data
    