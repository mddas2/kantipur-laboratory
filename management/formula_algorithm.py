from django.shortcuts import render,redirect
from django.http import HttpResponse
from .formula_serializers import SampleFormParameterFormulaCalculateReadSerializer
from .models import SampleFormParameterFormulaCalculate
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from .custompermission import MyPermission
from rest_framework import status
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

class Formula:
    def __init__(self,formula,parameter_id):
        self.formula = formula
        self.parameter_id = parameter_id

    def GetNumberOfFields():
        pass

    def getProperFieldsResponse():
        pass

    def calculate():
        pass

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
    
        