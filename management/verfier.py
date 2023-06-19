from django.shortcuts import render,redirect
from django.http import HttpResponse
from . verifier_serializer import SampleFormWriteVerifierSerilizer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory,TestResult, Payment
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import SampleFormVerifier
from .custompermission import SampleFormHasVerifierViewSetPermission
from . encode_decode import generateDecodeIdforSampleForm
from django.http import Http404

class SampleFormHasVerifierViewSet(viewsets.ModelViewSet):
    queryset = SampleFormVerifier.objects.all()
    serializer_class = SampleFormWriteVerifierSerilizer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name','id']

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['sample_form_id']
    filterset_fields = ['sample_form_id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SampleFormHasVerifierViewSetPermission]
    pagination_class = MyLimitOffsetPagination

    def get_object(self):
        user = self.request.user

        id = generateDecodeIdforSampleForm(self.kwargs['pk'],user) 

        queryset = self.get_queryset()
        obj = queryset.filter(id=id).first()
        if not obj:
            raise Http404("Object not found")

        return obj
    
    def get_queryset(self):
        query = SampleFormVerifier.objects.all()
        encoded_sample_form_id = self.request.query_params.get('sample_form_id')
        if encoded_sample_form_id is not None:              

            # Perform the decoding to obtain the actual sample form ID
            decoded_sample_form_id = generateDecodeIdforSampleForm(encoded_sample_form_id,self.request.user)

            # Use the decoded sample form ID to filter the queryset
            query = SampleFormVerifier.objects.filter(sample_form_id=decoded_sample_form_id)

        return query
   
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
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    