from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers.track_serializer import TrackSampleSerializer
from rest_framework.response import Response

# Create your views here.
class TrackSample(generics.RetrieveAPIView):
    queryset = SampleForm.objects.all()
    serializer_class = TrackSampleSerializer

    

    
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
