from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .raw_data_serializer import rawDataSerializer
from . encode_decode import generateDecodeIdforSampleForm
from django.http import HttpResponse

def generateRawData(sample_form_has_parameter_id,remarks):
    print(sample_form_has_parameter_id)
    
    obj = SampleFormHasParameter.objects.get(id=sample_form_has_parameter_id)
   
    formula_calculate_parameters = obj.formula_calculate.all()

    sample_form_id = obj.sample_form.id
    
    raw_data_sheet_instance = RawDataSheet(sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id,remarks=remarks,status=obj.status,analyst_user=obj.analyst_user)
    raw_data_sheet_instance.save()
    
    print(formula_calculate_parameters)
    for param in formula_calculate_parameters:
        print(param," md")
        data = {
            'raw_data_id':raw_data_sheet_instance.id,
            'parameter_id':param.parameter.id,
            'result':param.result,
            'is_verified':param.is_verified,
            'input_fields_value':param.input_fields_value,
            'auto_calculate_result':param.auto_calculate_result,
            'remark':param.remarks,
        }
        RawDataSheetDetail.objects.update_or_create(**data)
    return True

class rawDataDetail(generics.ListAPIView):
    # queryset = SampleForm.objects.all() 
    # serializer_class = CompletedSampleFormHasAnalystSerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']


    def get_queryset(self):

        sample_form_has_parameter_id = self.kwargs.get('sample_form_has_parameter')
        query = RawDataSheet.objects.filter(sample_form_has_parameter_id=sample_form_has_parameter_id)
        print(query)
    
        return query
    
    def get_serializer_class(self):
        serializer = rawDataSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

class rawDataForSampleForm(generics.ListAPIView):
    # queryset = SampleForm.objects.all() 
    # serializer_class = CompletedSampleFormHasAnalystSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']


    def get_queryset(self):

        sample_form_id = self.kwargs.get('sample_form')
        print(sample_form_id)
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,user) 
        print(sample_form_id)
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id)
    
        return query
    
    def get_serializer_class(self):
        serializer = rawDataSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
