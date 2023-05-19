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
            data =ReportAdminList(report_type,report_lang)
        elif report_name == "users-list":
            data = ReportUserList(report_type,report_lang)
        elif report_name == "user-with-sample-form":
            data = ReportUserSampleForm(report_type,report_lang)
        elif report_name == "sample-form":
            data = ReportSampleForm(report_type,report_lang)
        elif report_name == "commodity":
            data = ReportCommodity(report_type,report_lang)
        elif report_name == "parameter":
            data = ReportParameter(report_type,report_lang)
        else:
            data = {
                'error':"not match"
            }
            data = json.dumps(data)
        return HttpResponse(data)
        return HttpResponse(report_name+":"+report_type+":"+report_lang)
        return render(request, 'report.html')
       