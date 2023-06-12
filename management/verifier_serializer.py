from .models import SampleFormVerifier,SampleForm
from rest_framework import serializers

class SampleFormWriteVerifierSerilizer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormVerifier
        fields = '__all__'

    def validate(self, data):
        sample_form_id = data.get('sample_form')
        sample_form_obj = SampleForm.objects.get(id=sample_form_id)
        if sample_form_obj.is_analyst_test == False:
            raise serializers.ValidationError("Analyst have not sent sample test to supervisor.")

        return data
    