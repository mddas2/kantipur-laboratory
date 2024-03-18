from rest_framework  import serializers
from ..models import SampleForm

class IsBackSampleFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['name','condition','mfd','dfb','days_dfb','dfb_duration','dfb_type','batch','brand','purpose','requested_export','report_date','sample_type','sample_units','sample_quantity','number_of_sample','amendments','is_back','submit_back_remarks']


