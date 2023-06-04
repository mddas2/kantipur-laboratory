import json
from account.models import CustomUser
from management.models import SampleForm,Commodity,SampleFormHasParameter,CommodityCategory
from . serializers import CustomUserSerializer,CommodityCategorySerializer,SampleFormOnlySerializer,CommodityOnlySerializer,ClientCategorySerializer
from django.http import HttpResponse
import pandas as pd
# https://limsserver.kantipurinfotech.com.np/api/report/get-report/report_name/report_type/report_lang/
def ReportAdminList(report_type,report_lang,id=None):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report admin list pdf download </body></html>")


def ReportUserList(report_type,report_lang,id=None):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report user  list pdf download </body></html>")

def ReportUserRequest(report_type,report_lang,id=None):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report user  request pdf download </body></html>")
    


def ReportUserSampleForm(report_type,report_lang,id=None):
    query = SampleForm.objects.all()
    serializer_data = SampleFormOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report user has sample form pdf download </body></html>")

def ClientCategory(report_type,report_lang,id=None):
    from management.models import ClientCategory
    query = ClientCategory.objects.all()
    serializer_data = ClientCategorySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report client category form pdf download </body></html>")


def ReportSampleForm(report_type,report_lang,id=None):
    query = SampleForm.objects.all()
    serializer_data = SampleFormOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report sample form pdf download </body></html>")

def ReportCommodity(report_type,report_lang,id=None):
    query = Commodity.objects.all()
    serializer_data = CommodityOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report commodity pdf download </body></html>")

def ReportComodityCategory(report_type,report_lang,id=None):
    query = CommodityCategory.objects.all()
    serializer_data = CommodityCategorySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report commodity category pdf download </body></html>")


def ReportParameter(report_type,report_lang,id=None):
    query = Commodity.objects.all()
    serializer_data = CommodityOnlySerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    if report_type == "excel":
        # Create a response object with the appropriate content type
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

        # Write the DataFrame to an Excel file and save it to the response
        with pd.ExcelWriter(response, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        return response
    
    elif report_type == "pdf":
        # print("pdf")
        return HttpResponse("<html><body> this is report admin list pdf download </body></html>")

