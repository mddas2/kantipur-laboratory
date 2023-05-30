import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import views
import json
from management.models import SampleForm
from rest_framework import viewsets,status
from rest_framework.response import Response
from . sample_form_serializers import SampleFormHasAnalystSerializer
from . parameter_has_assigned_analyst import SampleFormHasParameterAnalystSerializer
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from management.pagination import MyLimitOffsetPagination
from .report_download import ReportAdminList,ReportParameter,ReportCommodity,ReportUserSampleForm,ReportUserList,ReportSampleForm
#report_type:['pdf','excel','csv']
#report_name:['admin-list','users-list','user-with-sample-form','sample-form','commodity','parameter']
class SampleFormHasAnalystAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        print(request.user.role)
        queryset = SampleForm.objects.filter(supervisor_user = request.user)
        serializer = SampleFormHasAnalystSerializer(queryset, many=True)
        return Response(serializer.data)

    # def post(self, request, format=None):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

#parameter has assigned user
class ParameterHasAssignedAnalyst(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        print(sample_form_id)
        print(request.user)
        queryset = SampleForm.objects.all()
        serializer = SampleFormHasParameterAnalystSerializer(queryset, many=True)
        return Response(serializer.data)


class ReportDownload(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
            