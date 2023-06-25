from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
def generateRawData(sample_form_has_parameter_id):
    print(sample_form_has_parameter_id)
    
    obj = SampleFormHasParameter.objects.get(id=sample_form_has_parameter_id)
   
    formula_calculate_parameters = obj.formula_calculate.all()

    sample_form_id = obj.sample_form.id
    
    raw_data_sheet_instance = RawDataSheet(sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id)
    raw_data_sheet_instance.save()
    
    for param in formula_calculate_parameters:
        data = {
            'parameter_id':param.parameter.id,
            'result':param.result,
            'is_verified':param.is_verified,
            'input_fields_value':param.input_fields_value,
            'auto_calculate_result':param.auto_calculate_result,
            'remark':param.remarks,
        }
        RawDataSheetDetail.objects.update_or_create(raw_data_id=raw_data_sheet_instance.id,defaults=data)
    return True
    
