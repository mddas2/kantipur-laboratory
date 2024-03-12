from rest_framework import serializers
from management.models import SampleForm

class TrackSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['id','name','namuna_code']

    