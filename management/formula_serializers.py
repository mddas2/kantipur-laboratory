from .models import SampleFormParameterFormulaCalculate
from rest_framework import serializers

class SampleFormParameterFormulaCalculateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormParameterFormulaCalculate
        fields = '__all__'
