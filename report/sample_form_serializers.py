from management.models import SampleForm, Commodity
from rest_framework import serializers


class SampleFormHasAnalystSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = '__all__'
