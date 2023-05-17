from django.shortcuts import render,redirect
from django.http import HttpResponse
from .formula_serializers import SampleFormParameterFormulaCalculateReadSerializer,FormulaApiCalculateSerializer,FormulaApiGetFieldSerializer
from .models import SampleFormParameterFormulaCalculate,Commodity,TestResult,SampleForm
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from .custompermission import MyPermission
from rest_framework import status
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import re

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

class Formula:
    def __init__(self,commodity_id,parameter_id,sample_form_id):
        self.commodity_id = commodity_id
        self.parameter_id = parameter_id
        self.sample_form_id  = sample_form_id

    def FullValidiate(self,formula_variable_fields_value):
        return True
    
    def HalfValidiate(self):
        return True
    
    def isParameterRelatedToCommodityAndSampleForm(self):
        return True

    def GetNumberOfFields(self):
        return 
    
    def GetQueryObject(self):#sample-form:3,commidiy:10,parameter:119
        # and sample_form_obj.parameters.filter(id=self.parameter_id).exists()
        sample_form_obj = SampleForm.objects.get(id=self.sample_form_id)
        commodity_id = sample_form_obj.commodity_id # if commodity is related to sample form commodity id
        # if str(commodity_id) == self.sample_form_id:
        test_obj = TestResult.objects.get(id=self.parameter_id)
        return test_obj
        return False
    
    def getFormulaVariable(self,formula):
        return re.findall(r'[A-Za-z]+', formula)
    
    def MakeProperResponse(self,variables,notations):
        return [{"name": var, "label": var, "value": ""} for var in variables]

    def getProperFieldsResponse(self):
        query_obj = self.GetQueryObject()
        if query_obj != False:
            #do some things.
            notations  = []
            formula =  query_obj.formula
            # print(formula)
            variables = self.getFormulaVariable(formula)
            response = self.MakeProperResponse(variables,notations)
            # print(response)
        else:
            response = {
                    "error":"data not match",
                    'status':status.HTTP_404_NOT_FOUND                    
                }
            # return Response(response, status=status.HTTP_404_NOT_FOUND)
            print("parameter or commidity id not related to sample form id.")

        return response

    def calculate(self,formula_variable_fields_value):
        pass
    
    def Save(self,result):
        pass

class FormulaApiCalculate(APIView):
 
    def post(self, request, format=None):

        serializer = FormulaApiCalculateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Get validated data
        commodity_id = serializer.validated_data['commodity_id']
        parameter_id = serializer.validated_data['parameter_id']
        sample_form_id = serializer.validated_data['sample_form_id']
        formula_variable_fields_value = serializer.validated_data['formula_variable_fields_value']

        formula_obj = Formula(commodity_id,parameter_id,sample_form_id)
        if formula_obj.FullValidiate(formula_variable_fields_value) == True:
            result = formula_obj.calculate(formula_variable_fields_value)
            formula_obj.Save(result)
            response_data = {
                'message': "formula calculate !!!",            
            }
        else:
            # Create the response data
            response_data = {
                'message': "some things went wrong",            
            }

        return Response(response_data)

class FormulaApiGetFields(APIView):
    def get(self, request, format=None):
        response_data = {
            'number_of_field': 3,
            'fields':[
                {
                'name':"l",
                'label':'Length',
                'value':'',

            },
            {
                'name':"b",
                'label':'Breadth',
                'value':'',

            },
             {
                'name':"h",
                'label':'Height',
                'value':'',

            }
        ]

    }
        return Response(response_data)
    
    def post(self, request, format=None):
        # Deserialize the request data
        serializer = FormulaApiGetFieldSerializer(data=request.data)
        if serializer.is_valid():
            # Get validated data
            commodity_id = serializer.validated_data['commodity_id']
            parameter_id = serializer.validated_data['parameter_id']
            sample_form_id = serializer.validated_data['sample_form_id']

            formula_obj = Formula(commodity_id,parameter_id,sample_form_id)
            if formula_obj.HalfValidiate()==True:
                response = formula_obj.getProperFieldsResponse()
                response_data = response
            else:
                response_data = {
                    'message':"Some thing went wrong"
                }
        else:
            return Response(serializer.errors, status=400)
    

        return Response(response_data)



class SampleFormParameterFormulaCalculateViewSet(viewsets.ModelViewSet):
    queryset = SampleFormParameterFormulaCalculate.objects.all()
    serializer_class = SampleFormParameterFormulaCalculateReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    filterset_fields = ['id']
    ordering_fields = ['id']
    
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    pagination_class = MyLimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SampleFormParameterFormulaCalculateReadSerializer
        return super().get_serializer_class()
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "created successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)
    
        