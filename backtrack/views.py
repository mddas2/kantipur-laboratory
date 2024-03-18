from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers.track_serializer import TrackSampleSerializer
from .serializers.samplebackserializer import IsBackSampleFormSerializer
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from management.models import SampleForm
from management.serializers import SampleFormRetrieveSerializer
from management.pagination import MyLimitOffsetPagination,MyPageNumberPagination
from django.http import Http404
from management.encode_decode import generateDecodeIdforSampleForm
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.
class TrackSample(generics.RetrieveAPIView):
    queryset = SampleForm.objects.all()
    serializer_class = TrackSampleSerializer


class BackSampleFormViewset(viewsets.ModelViewSet):

    queryset = SampleForm.objects.all()
    serializer_class = SampleFormRetrieveSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user_obj__email','status','form_available','commodity__name','refrence_number','sample_lab_id']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'client_category_detail__client_category':['exact'],
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyPageNumberPagination

    def get_object(self):
        user = self.request.user
        id = generateDecodeIdforSampleForm(self.kwargs['pk'],user) 
        queryset = self.get_queryset()
        obj = queryset.filter(id=id).first()
        if not obj:
            raise Http404("Object not found")
        return obj
    
    def get_queryset(self):
        user = self.request.user
        if self.action == 'is_back_sample':
            query = SampleForm.objects.filter(is_back = 'smu_back')
        elif self.action == 'back_sample_forward':
            query = SampleForm.objects.filter(is_back = 'smu_back')
        return query
    
    def get_serializer_class(self):
        if self.action == 'is_back_sample':
            return IsBackSampleFormSerializer
    
    @action(detail=True, methods=['put'],name="is_back_sample", url_path="back-sample-smu")
    def is_back_sample(self, request,pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "Sample updated successfully",
            "data": serializer.data
        }
        return Response({"message": "update formal form successful"}, status=status.HTTP_200_OK)
    

    @action(detail=True, methods=['put'],name="back_sample_forward", url_path="back-sample-forward")
    def back_sample_forward(self, request,pk=None):
        instance = self.get_object()
        instance.is_back = None
        instance.submit_back_remarks = request.data.get('forward_remarks')
        instance.save()
        response_data = {
            "message": "Sample updated successfully",
        }

        return Response({"message": "update formal form successful"}, status=status.HTTP_200_OK)
