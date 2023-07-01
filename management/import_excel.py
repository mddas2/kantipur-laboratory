from django.http import FileResponse
from django.conf import settings
from django.http import HttpResponse
import os
from rest_framework.response import Response
import pandas as pd
from django.http import JsonResponse

from .models import Commodity,CommodityCategory,TestResult,SampleForm

def ImportExcel(request):
    # CommodityCategory.objects.all().delete()
    # SampleForm.objects.all().delete()
    # return HttpResponse("deleted successfully!!!....")
    
    file_path = os.path.join(settings.MEDIA_ROOT, "import_data/lims_data.xlsx")
    print(file_path)

    if os.path.exists(file_path):
        df = pd.read_excel(file_path)
        for index, row in df.iterrows():
            
            commodity_category = row['commodity_category']
            commodity_category_nepali = row['commodity_cat_nepali']

            commodity_name = row['commodity_name']
            commodity_name_nepali = row['commodity_name_nepali']

            test_type = row['test_type']
            test_type_nepali = row['test_type_nepali']

            parameters_name = row['parameter']
            parameters_nepali = row['parameter_nepali']

            ref_test_method = row['ref._test_methods']

            commodity_test_duration = row['commodity_test_duration']

            unit = row['units']
            unit_nepali = row['units_nepali']

            mandatory_standard = row['mandatory_standard']
            mandatory_standard_nepali = row['mandatory_standard_nepali']

            formula = row['formula']

            notation = row['abbreviation']

            remarks = row['remarks']

            commodity_price = row['commodity_price']
            parameter_price = row['paramater_price']

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
            commodity_id = Commodity.objects.get(name=commodity_name).id
            test_result = { #parameter
                'commodity_id' : commodity_id,
                'name' : parameters_name,
                'name_nepali' : parameters_nepali,
                'ref_test_method' : ref_test_method,
                'units' : unit,
                'units_nepali' : unit_nepali,
                'price' : parameter_price,
                'mandatory_standard' : mandatory_standard,
                'mandatory_standard_nepali' : mandatory_standard_nepali,
                'remarks' : remarks,
                'test_type' : test_type,
                'test_type_nepali' : test_type_nepali,
                'formula_notation' : notation,
                'formula' : formula,
            }
            testresult_obj,create_test_result = TestResult.objects.update_or_create(commodity_id = commodity_id ,name = parameters_name, defaults = test_result)
            if create_test_result:
                print("parameter created successfully")

        top_10 = df.head(10)
        # print(top_10)
        data = top_10.to_json(orient='records')
        return JsonResponse(data, safe=False)