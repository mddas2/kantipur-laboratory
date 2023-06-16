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
from . analyst_final_report_serializer import DetailSampleFormHasParameterRoleAsAnalystSerializer
from . parameter_has_assigned_analyst_detail import DetailSampleFormHasParameterAnalystSerializer,DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp
from . verifier_has_completed_sample_form import CompletedSampleFormHasVerifierSerializer
from django.shortcuts import render
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from management.pagination import MyLimitOffsetPagination
from django.db.models import Q
from management import roles
from rest_framework import generics
from .report_download import ReportAdminList,ReportParameter,ReportCommodity,ReportUserSampleForm,ReportUserList,ReportSampleForm,ReportUserRequest,ReportComodityCategory,FinalReport
#report_type:['pdf','excel','csv']
#report_name:['admin-list','users-list','user-with-sample-form','sample-form','commodity','parameter']
#['sample-request','user-request','client-category','commodity-with-parameter','commodity-category','commodity','parameter']
class SampleFormHasAnalystAPIView(generics.ListAPIView):
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'owner_user': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'supervisor_user': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self): 
        return SampleFormHasAnalystSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SampleForm.objects.filter(Q(supervisor_user = request.user) & ~Q(status="completed") & ~Q(status="not_assigned")).order_by("-created_date")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    
class CompletedSampleFormHasVerifierAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'owner_user': ['exact'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'supervisor_user': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }

    def get_serializer_class(self): 
        return CompletedSampleFormHasVerifierSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False)).order_by("-created_date")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#parameter has assigned user

class ParameterHasAssignedAnalyst(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        queryset = SampleForm.objects.filter(id=sample_form_id).first()
        serializer = SampleFormHasParameterAnalystSerializer(queryset,many = False)
        return Response(serializer.data)

class DetailParameterHasAssignedAnalyst(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        if self.request.user.role == roles.ANALYST:
            queryset = SampleForm.objects.filter(id=sample_form_id).first()
            serializer = DetailSampleFormHasParameterAnalystSerializer(queryset,many = False,context={'request': request})
        else:
            print("smu detail")
            queryset = SampleForm.objects.filter(id=sample_form_id).first()
            serializer = DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp(queryset,many = False,context={'request': request})
        return Response(serializer.data)
        
class ReportDownload(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request,report_name,report_type,report_lang,id=None):
        if report_name == "users-list":
            response = ReportUserList(report_type,report_lang,id)
            return response
            # return data
        elif report_name == "users-list":
            response = ReportUserList(report_type,report_lang,id)
            return response
        
        elif report_name == "user-request":
            response = ReportUserRequest(report_type,report_lang,id)
            return response
        
        elif report_name == "sample-request":
            response = ReportUserSampleForm(report_type,report_lang,id)
            return response
        
        elif report_name == "client-category":
            response = ReportSampleForm(report_type,report_lang,id)
            return response
        
        elif report_name == "commodity-with-parameter":
            response = ReportCommodity(report_type,report_lang,id)
            return response
        elif report_name == "commodity-category":
            response = ReportComodityCategory(report_type,report_lang,id)
            return response
        
        elif report_name == "commodity":
            response = ReportCommodity(report_type,report_lang,id)
            return response
        
        elif report_name == "parameter":
            response = ReportParameter(report_type,report_lang,id)
            return response
                
        if report_name == "final-report":
            response = FinalReport(report_type,report_lang,id)
            return response
        else:
            data = {
                'error':"not match"
            }
            data = json.dumps(data)
            return HttpResponse(data)
            
def FinalReportPdf(request):
    from django.template.loader import get_template
    from xhtml2pdf import pisa
    template = get_template('final_report.html')
    context = {'data': 'Hello, World!'}  # Example context data

    # Render the template with the context
    html = template.render(context)

    # Create a PDF object
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="output.pdf"'

    # Generate the PDF from the HTML content
    pisa.CreatePDF(html, dest=response)

    return response
    return HttpResponse("pdf")