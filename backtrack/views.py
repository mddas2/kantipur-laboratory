from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .serializers.track_serializer import TrackSampleSerializer
from rest_framework.response import Response
from management.models import SampleForm
from rest_framework.decorators import action
from rest_framework import status

# Create your views here.
class TrackSample(generics.RetrieveAPIView):
    queryset = SampleForm.objects.all()
    serializer_class = TrackSampleSerializer

