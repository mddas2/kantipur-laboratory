from .models import RawDataSheet,RawDataSheetDetail,TestResult,SampleFormHasParameter
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .raw_data_serializer import rawDataSerializer,rawDataTestTypeSerializer,rawDataTestTypeGlobalSerializer
from . encode_decode import generateDecodeIdforSampleForm
from django.http import HttpResponse

def generateRawData(sample_form_has_parameter_id,remarks):
    print(sample_form_has_parameter_id)
    
    obj = SampleFormHasParameter.objects.get(id=sample_form_has_parameter_id)
   
    formula_calculate_parameters = obj.formula_calculate.all()

    sample_form_id = obj.sample_form.id
    supervisor_remarks = obj.sample_form.remarks

    super_visor_sample_form_id = obj.super_visor_sample_form.id

    test_type2 = obj.parameter.all().first().test_type

    print("data generating test type ",test_type2)

    raw_data_sheet_instance = RawDataSheet(super_visor_sample_form_id = super_visor_sample_form_id ,sample_form_id=sample_form_id,sample_form_has_parameter_id = obj.id,remarks=remarks,status="not_verified",analyst_user=obj.analyst_user,supervisor_remarks=supervisor_remarks,test_type = test_type2)
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

def UpdategenerateRawData(supervisor_table_id,remarks):
   raw_data_sheet_supervisor =  RawDataSheet.objects.filter(super_visor_sample_form_id = supervisor_table_id)
   raw_data_sheet_supervisor.update(supervisor_remarks = remarks)
   print("remarks added to supervisor")
   


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
    
class rawDataForSampleFormTestType(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        sample_form_id = self.kwargs.get('sample_form')
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id, user)
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id, super_visor_sample_form__supervisor_user=user.id)
        return query
    
    def get_serializer_class(self):
        return rawDataTestTypeSerializer
        
    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        test_type_data = {}
        for item in data:
            test_type = item.pop('test_type')
            if test_type not in test_type_data:
                test_type_data[test_type] = []
            test_type_data[test_type].append(item)

        response = {}
        for test_type, test_type_values in test_type_data.items():
            response[test_type] = test_type_values

        return Response(response)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    
class rawDataForSampleFormGlobal(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
  
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']

    def get_queryset(self):
        sample_form_id = self.kwargs.get('sample_form')
        user = self.request.user
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id, user)
        query = RawDataSheet.objects.filter(sample_form_id=sample_form_id)#.filter(Q(status = "not_approved") status= "not_verified") blunder fix
        return query
    
    def get_serializer_class(self):
        return rawDataTestTypeGlobalSerializer
        
    def list(self, request, *args, **kwargs):
        from rest_framework.response import Response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        test_type_data = {}
        for item in data:
            test_type = item.pop('test_type')
            if test_type not in test_type_data:
                test_type_data[test_type] = []
            test_type_data[test_type].append(item)

        response = {}
        for test_type, test_type_values in test_type_data.items():
            response[test_type] = test_type_values

        return Response(response)
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)