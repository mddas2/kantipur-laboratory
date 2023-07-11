from rest_framework import serializers
from management.models import SuperVisorSampleForm,ClientCategory, SampleForm, Commodity, CommodityCategory , TestResult ,SampleFormHasParameter,Payment,SampleFormParameterFormulaCalculate

class TestResultSerializer(serializers.ModelSerializer):
    class Meta:
        ref_name = "supervisorfinalreportTestResult"
        model = TestResult
        fields = '__all__'

class SupervisorFinalReportSerializer(serializers.ModelSerializer):
    parameters = TestResultSerializer(read_only = True)
    class Meta:
        ref_name = "supervisorfinalreportSuperVisorSampleForm"
        model = SuperVisorSampleForm
        fields = '__all__'

    