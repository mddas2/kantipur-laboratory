import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import views
import json
from . report_download import ReportAdminList,ReportUserList,ReportUserSampleForm,ReportSampleForm,ReportCommodity,ReportParameter

from django.shortcuts import render
#report_type:['pdf','excel','csv']
#report_name:['admin-list','users-list','user-with-sample-form','sample-form','commodity','parameter']

class ReportDownload(views.APIView):
    def get(self, request,report_name,report_type,report_lang):
        if report_name == "admin-list":
            response =ReportAdminList(report_type,report_lang)
            return response
            # return data
        elif report_name == "users-list":
            response = ReportUserList(report_type,report_lang)
            return response
        elif report_name == "user-with-sample-form":
            response = ReportUserSampleForm(report_type,report_lang)
            return response
        elif report_name == "sample-form":
            response = ReportSampleForm(report_type,report_lang)
            return response
        elif report_name == "commodity":
            response = ReportCommodity(report_type,report_lang)
            return response
        elif report_name == "parameter":
            response = ReportParameter(report_type,report_lang)
            return response
        else:
            data = {
                'error':"not match"
            }
            data = json.dumps(data)
            return HttpResponse(data)
            