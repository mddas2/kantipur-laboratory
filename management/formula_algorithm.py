from django.shortcuts import render,redirect
from django.http import HttpResponse
from .formula_serializers import SampleFormParameterFormulaCalculateReadSerializer,FormulaApiCalculateSerializer,FormulaApiGetFieldSerializer,FormulaApiCalculateSaveSerializer
from .models import SampleFormParameterFormulaCalculate,Commodity,TestResult,SampleForm
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
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
        if str(commodity_id) == str(self.commodity_id) and sample_form_obj.parameters.filter(id=self.parameter_id).exists():
            test_obj = TestResult.objects.get(id=self.parameter_id)
            return test_obj
        return False
    
    def getFormulaVariable(self,formula):
        variables =  re.findall(r'[A-Za-z]+', formula)
        variables = list(set(variables))
        print(variables)
        return variables

    
    def MakeProperResponse(self,variables,notations):
        field =  [{"name": var, "label": var, "value": ""} for var in variables]
        return {
            'fields' : field
        }

    def getProperFieldsResponse(self):
        query_obj = self.GetQueryObject()
        if query_obj != False:
            #do some things.
            notations  = []
            formula =  query_obj.formula
            variables = self.getFormulaVariable(formula)
            response = self.MakeProperResponse(variables,notations)
            return response
        else:
            response = {
                    "error":"data not match",
                    'status':status.HTTP_404_NOT_FOUND                    
                }
            # return Response(response, status=status.HTTP_404_NOT_FOUND)
            print("parameter or commidity id not related to sample form id.")

        return response

    def calculate(self,formula_variable_fields_value):
        import json
        query_obj = self.GetQueryObject()
        formula = query_obj.formula

        if '{' or '[' in formula:
            formula = formula.replace('[', '(').replace(']', ')')
            formula = formula.replace('{', '(').replace('}', ')')
        
    

        json_values = json.loads(formula_variable_fields_value)

        error = {}
        error = 0
        result = 0
        is_error_occured = False
        try:
            result = eval(formula, json_values)
            result = round(result, 3)
        except ZeroDivisionError:
            is_error_occured = True
            error = {'message': 'Division by zero', 'status': status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            is_error_occured = True
            error = {'message': f'Error: {str(e)}', 'status': status.HTTP_400_BAD_REQUEST}
    
        return is_error_occured,error,result    
    
    def Save(self,result,input_fields_value):
        data = {
            'result' : result,
            'input_fields_value' : input_fields_value,
        }
        # obj_result,create = SampleFormParameterFormulaCalculate.objects.update_or_create(sample_form_id = self.sample_form_id, parameter_id = self.parameter_id, commodity_id = self.commodity_id,defaults=data)
        return result
    
class FormulaGetToVerifier(APIView):
    def get(self, request, sample_form_id, format=None):
        queryset = SampleFormParameterFormulaCalculate.objects.filter(sample_form_id=sample_form_id)
        serializer = SampleFormParameterFormulaCalculateReadSerializer(queryset, many=True)
        return Response(serializer.data)
       
class FormulaApiCalculate(APIView): 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):

        serializer = FormulaApiCalculateSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get validated data
        commodity_id = serializer.validated_data['commodity']
        parameter_id = serializer.validated_data['parameter']
        sample_form_id = serializer.validated_data['sample_form']
        formula_variable_fields_value = serializer.validated_data['formula_variable_fields_value']


        formula_obj = Formula(commodity_id,parameter_id,sample_form_id)
        if formula_obj.FullValidiate(formula_variable_fields_value) == True:
            is_error_occured,error,result = formula_obj.calculate(formula_variable_fields_value)
            if is_error_occured:
                res = {
                    'message' : error['message']
                }
                response_data = res
                response_status = error['status']
            else:
                result = formula_obj.Save(result,formula_variable_fields_value)
                if result:
                    response_data = {
                        'message': "formula returned !!!",
                        'result' : result,
                        'formula_variable_fields_value' : formula_variable_fields_value
                    }
                    response_status = status.HTTP_200_OK
                else:
                    response_data = {
                        'message': "formula can not calculate error",   
                    }
                    response_status = status.HTTP_404_NOT_FOUND

        else:
            # Create the response data
            response_data = {
                'message': "some things went wrong",            
            }
            status.HTTP_400_BAD_REQUEST

        return Response(response_data, status=response_status)

class FormulaApiGetFields(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        
        serializer = FormulaApiGetFieldSerializer(data=request.data,context={'request': request})
        if serializer.is_valid():
            # Get validated datas
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


class FormulaApiCalculateSave(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
 
    def post(self, request, format=None):

        serializer = FormulaApiCalculateSaveSerializer(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)

        # Get validated data
        commodity_id = serializer.validated_data['commodity']
        parameter_id = serializer.validated_data['parameter']
        sample_form_id = serializer.validated_data['sample_form']
        # formula_variable_fields_value = serializer.validated_data['formula_variable_fields_value']
        result = serializer.validated_data['result']
        data = {
            'result' : result,
        }

        data,created = SampleFormParameterFormulaCalculate.objects.update_or_create(sample_form_id = sample_form_id, parameter_id =parameter_id, commodity_id = commodity_id,defaults=data)
        message = {
            "message":"save successfully"
        }
    
        return Response(message, status=status.HTTP_200_OK)