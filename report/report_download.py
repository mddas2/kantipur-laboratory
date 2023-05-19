import json
from account.models import CustomUser
from . serializers import CustomUserSerializer
from django.http import HttpResponse
import pandas as pd
def ReportAdminList(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def ReportUserList(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def ReportUserSampleForm(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def ReportSampleForm(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def ReportCommodity(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response

def ReportParameter(report_type,report_lang):
    query = CustomUser.objects.all()
    serializer_data = CustomUserSerializer(query, many=True)
    serialized_data = serializer_data.data
    df = pd.DataFrame.from_records(serialized_data)

    # Create a response object with the appropriate content type
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="data.xlsx"'

    # Write the DataFrame to an Excel file and save it to the response
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)

    return response
