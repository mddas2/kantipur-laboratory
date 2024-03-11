from django.http import HttpResponse
from rest_framework import views
import json
from management.models import SampleForm,SuperVisorSampleForm,SampleFormHasParameter
from rest_framework.response import Response
from . sample_form_serializers import SampleFormHasSupervisorParameterSerializer
from . supervisor_final_report_serializer import SupervisorFinalReportSerializer
from . parameter_has_assigned_analyst import SampleFormHasParameterAnalystSerializer,SampleFormTrackbyAnalystSerializer
from . parameter_has_assigned_analyst_detail import DetailSampleFormHasParameterAnalystSerializer,DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp,FinalReportNepaliAnalystSerializer
from . verifier_has_completed_sample_form import CompletedSampleFormHasVerifierSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from management.pagination import MyPageNumberPagination
from django.db.models import Q,Max
from account import roles
from rest_framework import generics
from .report_download import TestReport,ReportParameter,ReportCommodity,ReportUserSampleForm,ReportUserList,ReportSampleForm,ReportUserRequest,ReportComodityCategory,FinalReport,rawDataSheetAnalystReport
from management.encode_decode import generateDecodeIdforSampleForm,generateDecodeIdByRoleforSampleForm
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action

class SampleFormHasAnalystAPIView(generics.ListAPIView):
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','sample_form__code','sample_form__id','sample_form__namuna_code','sample_form__sample_lab_id','sample_form__namuna_code']
    ordering_fields = ['id']
    filterset_fields = {
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'status':['exact'],
        'sample_form__client_category_detail__client_category':['exact']
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self): 
        return SampleFormHasSupervisorParameterSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SuperVisorSampleForm.objects.filter(supervisor_user = request.user).filter(~Q(sample_form__status="completed") & ~Q(status="not_assigned") & ~Q(sample_form__client_category_detail__client_category=12)).annotate(max_created=Max('sample_has_parameter_analyst__created_date')).order_by('-max_created')
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
class FormalSampleForm_SampleFormHasAnalystAPIView(generics.ListAPIView):
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','sample_form__code','sample_form__id','sample_form__namuna_code','sample_form__sample_lab_id','sample_form__namuna_code']
    ordering_fields = ['id']
    filterset_fields = {
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'status':['exact'],
        'sample_form__client_category_detail__client_category':['exact']
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self): 
        return SampleFormHasSupervisorParameterSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SuperVisorSampleForm.objects.filter(supervisor_user = request.user).filter(~Q(sample_form__status="completed") & ~Q(status="not_assigned") & Q(sample_form__client_category_detail__client_category=12)).annotate(max_created=Max('sample_has_parameter_analyst__created_date')).order_by('-max_created')
        return queryset
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    
class SampleFormHasAnalystFinalReportAPIView(generics.ListAPIView): #supervisor final report
    
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    filterset_fields = {
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get_serializer_class(self): 
        return SampleFormHasSupervisorParameterSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SuperVisorSampleForm.objects.filter(supervisor_user = request.user).filter(sample_form__status="completed").order_by("-created_date")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    

class DetailSampleFormHasAnalystFinalReportAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, supervisor_table_id, format=None):
        queryset = SuperVisorSampleForm.objects.filter(id=supervisor_table_id).first()
        serializer = SupervisorFinalReportSerializer(queryset,many = False)
        return Response(serializer.data)

    
class CompletedSampleFormHasVerifierAPIView(generics.ListAPIView): #blunder md , permission fixed
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user_obj__name','status','form_available','commodity__name','namuna_code','code']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }

    def get_serializer_class(self): 
        return CompletedSampleFormHasVerifierSerializer
    
    def get_queryset(self):
        request = self.request
        if request.user.role == roles.VERIFIER:
            queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False) and Q(status="not_verified")).order_by("-created_date")
        else:
            raise PermissionDenied("You do not have permission to access thais resource.")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class notApprovedSampleFormHasAdminAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user_obj__name','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }

    def get_serializer_class(self): 
        return CompletedSampleFormHasVerifierSerializer
    
    def get_queryset(self):
        request = self.request
        queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True)).filter(status="not_approved").order_by("-created_date")
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

#parameter has assigned user
class SampleFormTrackbyAnalyst(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,request.user)
        queryset = SampleFormHasParameter.objects.filter(sample_form_id=sample_form_id)
        serializer = SampleFormTrackbyAnalystSerializer(queryset,many = True)
        return Response(serializer.data)

class ParameterHasAssignedAnalyst(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, sample_form_id, format=None):
        queryset = SampleForm.objects.filter(id=sample_form_id).first()
        serializer = SampleFormHasParameterAnalystSerializer(queryset,many = False)
        return Response(serializer.data)

class DetailParameterHasAssignedAnalyst(views.APIView): #it is used by sample report by superadmin, where non necessary fields are also providing, for sample report
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, sample_form_id, format=None):
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,request.user)
      
        if self.request.user.role == roles.ANALYST:
            queryset = SampleForm.objects.filter(id=sample_form_id).first()
            serializer = DetailSampleFormHasParameterAnalystSerializer(queryset,many = False,context={'request': request})
        else:#for superadmin,smu
            queryset = SampleForm.objects.filter(id=sample_form_id).first()
            serializer = DetailSampleFormHasParameterRoleAsAnalystSerializer_Temp(queryset,many = False,context={'request': request})
        return Response(serializer.data)
    

class FinalReportNepali(views.APIView):

    def get(self, request, sample_form_id,role_id, format=None):
        id = generateDecodeIdByRoleforSampleForm(sample_form_id,role_id)
        queryset = SampleForm.objects.filter(id=id).first()
        # print(queryset)
        serializer = FinalReportNepaliAnalystSerializer(queryset,many = False)
        return Response(serializer.data)
        
class ReportDownload(views.APIView):
    def get(self, request,report_name,report_type,report_lang,id=None,role=None):
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
        
        elif report_name == "test-report-sheet":
            sample_form_id =id
            response = TestReport(request,report_type,report_lang,sample_form_id,role)
            return response
                
        if report_name == "final-report":
            response = FinalReport(request,report_type,report_lang,id,role)
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

class rawDataReportDownload(views.APIView):
    def get(self, request,download_print=None,report_lang=None,sample_form_has_parameter=None):
        
        response = rawDataSheetAnalystReport(request,download_print,sample_form_has_parameter)
        return response

class rawDataReportApi(views.APIView):
    def get(self, request,download_print=None,report_lang=None,sample_form_has_parameter=None):
        
        response = rawDataSheetAnalystReport(request,download_print,sample_form_has_parameter)
        return response