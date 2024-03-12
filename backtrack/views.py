from django.shortcuts import render
from rest_framework import generics
from management.models import SampleForm
from .serializers.serializer import TrackSampleSerializer

# Create your views here.
class TrackSample(generics.RetrieveAPIView):
    queryset = SampleForm.objects.all()
    serializer_class = TrackSampleSerializer
    
