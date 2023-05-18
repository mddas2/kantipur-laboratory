from .models import SampleFormParameterFormulaCalculate
from rest_framework import serializers

class SampleFormParameterFormulaCalculateReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormParameterFormulaCalculate
        fields = '__all__'

class FormulaApiCalculateSerializer(serializers.Serializer):
    commodity = serializers.IntegerField()#serializers.CharField()
    parameter = serializers.IntegerField()
    sample_form = serializers.IntegerField()
    # formula_variable_fields_value = serializers.CharField()

class FormulaApiGetFieldSerializer(serializers.Serializer):
    commodity_id = serializers.IntegerField()
    parameter_id = serializers.IntegerField()
    sample_form_id = serializers.IntegerField()

    def validate(self, data):
        commodity_id = data.get('commodity_id')
        parameter_id = data.get('parameter_id')
        sample_form_id = data.get('sample_form_id')

        # Perform your validation logic
        if commodity_id and parameter_id and sample_form_id:
            pass
            # Example validation condition
            # if commodity_id == 1 and parameter_id == 2 and sample_form_id == 3:
            #     raise serializers.ValidationError("Invalid combination of commodity, parameter, and sample form.")

        # Return the validated data
        return data
 