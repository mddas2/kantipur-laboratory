from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
def generateRawData(sample_form_has_parameter_id):
    obj = SampleFormHasParameter.objects.get(sample_form_has_parameter_id)

    formula_calculate_parameters = obj.formula_calculate.all()

    sample_form_id = obj.sample_form.id
    
    raw_data_sheet_instance = RawDataSheet(sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id)
    raw_data_sheet_instance.save()

    for param in formula_calculate_parameters:
        data = {
            'parameter':param.parameter.id,
            'result':param.result,
            'is_verified':param.is_verified,
            'input_fields_value':param.input_fields_value,
            'auto_calculate_result':param.auto_calculate_result,
            'remark':param.remark,
        }
        RawDataSheetDetail.objects.update_or_create(raw_data=raw_data_sheet_instance.id,defaults=data)
        
    
