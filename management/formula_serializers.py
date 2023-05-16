from .models import SampleFormParameterFormulaCalculate
from rest_framework import serializers

class SampleFormParameterFormulaCalculateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormParameterFormulaCalculate
        fields = '__all__'

class FormulaApiCalculateSerializer(serializers.Serializer):
    commodity_id = serializers.IntegerField()#serializers.CharField()
    parameter_id = serializers.IntegerField()
    sample_form_id = serializers.IntegerField()
    formula_variable_fields_value = serializers.JSONField()

class FormulaApiGetFields(serializers.Serializer):
    commodity_id = serializers.IntegerField()#serializers.CharField()
    parameter_id = serializers.IntegerField()
    sample_form_id = serializers.IntegerField()

 