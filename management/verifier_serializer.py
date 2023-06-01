from .models import SampleFormVerifier,SampleForm
from rest_framework import serializers

class SampleFormWriteVerifierSerilizer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormVerifier
        fields = '__all__'