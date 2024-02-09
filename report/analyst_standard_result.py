def getStandardResult(formula_obj_result):
    if formula_obj_result.first().analyst_remarks:
       return formula_obj_result.first().analyst_remarks
    elif formula_obj_result.first().converted_result:
        return formula_obj_result.first().converted_result
    else:
        return formula_obj_result.first().result