from django.http import FileResponse
from django.conf import settings
from django.http import HttpResponse
import os
from rest_framework.response import Response
import pandas as pd
from django.http import JsonResponse
from django.shortcuts import render
from .serializers import TestResultSerializer
from .models import Commodity,CommodityCategory,TestResult,SampleForm

def ImportExcel(request):
    # CommodityCategory.objects.all().delete()
    # SampleForm.objects.all().delete()
    # return HttpResponse("deleted successfully!!!....")
    
    if request.POST:
        file = request.FILES.get('file')
    else:
        return render(request, 'excel_import.html')

    file_path = file
 
    df = pd.read_excel(file_path)
    for index, row in df.iterrows():
        
        commodity_category = row['commodity_category']
        commodity_category_nepali = row['commodity_cat_nepali']

        commodity_name = row['commodity_name']
        commodity_name_nepali = row['commodity_name_nepali']

        test_type = row['test_type']
        test_type_nepali = row['test_type_nepali']

        parameters_name = row['parameters']
        try:
            parameters_nepali = row['parameter_nepali']
        except:
            parameters_nepali = parameters_name

        ref_test_method = row['ref._test_methods']

        commodity_test_duration = row['commodity_test_duration']

        unit = row['units']
        unit_nepali = row['units_nepali']

        mandatory_standard = row['mandatory_standard']
    
        mandatory_standard_nepali = row['mandatory_standard_nepali']

        formula = row['formula']

        try:
            notation = row['abbreviation']
        except:
            notation = ""

        remarks = row['remarks']

        commodity_price = row['commodity_price']
        try:
            commodity_price = int(commodity_price)
        except:
            commodity_price = 0
        
        parameter_price = row['parameter_price']
        try:
            parameter_price = int(parameter_price)
        except:
            parameter_price = 0
    
        # return HttpResponse(parameter_price)

        commodity_category_data = {
            'name' : commodity_category,
            'name_nepali' : commodity_category_nepali,
        }


        try:
            commodity_category_obj = CommodityCategory.objects.create(**commodity_category_data)
        except:
            print("can not create")
        commodity_category_id = CommodityCategory.objects.get(name=commodity_category).id
        commodity_data = {
            'category_id' : commodity_category_id,
            'name' : commodity_name,
            'name_nepali':commodity_name_nepali,
            'units' : unit,
            'price' : commodity_price,
            'test_duration' : commodity_test_duration,
        }
        commodity_obj,create = Commodity.objects.update_or_create(name = commodity_name, defaults= commodity_data)
        if create:
            print("commodity created")

        multiple_units,multiple_mandatory_standard,multiple_ref_test_method = multipleUnitsMandatoryRefTestMethod(unit,unit_nepali,ref_test_method,mandatory_standard,mandatory_standard_nepali)

        commodity_id = Commodity.objects.get(name=commodity_name).id
        test_result = { #parameter
            'commodity_id' : commodity_id,
            'name' : parameters_name,
            'name_nepali' : parameters_nepali,
            'test_method' : multiple_ref_test_method,
            'units' : multiple_units,
            'price' : parameter_price,
            'mandatory_standard' : multiple_mandatory_standard,
            'remarks' : remarks,
            'test_type' : test_type,
            'test_type_nepali' : test_type_nepali,
            'formula_notation' : notation,
            'formula' : formula,
        }
        print(test_result)

        param_update_or_create = TestResult.objects.filter(commodity_id = commodity_id ,name = parameters_name)
        if param_update_or_create.exists():
            print("already exists..")
            pass
        else:
            serializer = TestResultSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            print("parameter created successfully")
            

    top_10 = df.head(10)
    # print(top_10)
    data = top_10.to_json(orient='records')
    return JsonResponse(data, safe=False)

def multipleUnitsMandatoryRefTestMethod(unit,unit_nepali,ref_test_method,mandatory_standard,mandatory_standard_nepali):
    return [1],[1],[1]