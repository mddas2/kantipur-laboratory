from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
def generateRawData(sample_form_has_parameter_id):
    obj = SampleFormHasParameter.objects.get(sample_form_has_parameter_id)
    parameters = obj.parameter.all()

    sample_form_id = obj.sample_form.id
    
    raw_data_sheet_instance = RawDataSheet(sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id)
    raw_data_sheet_instance.save()

    for param in parameters:
        # param_id = 
        pass
    id = raw_data_sheet_instance.id
    
