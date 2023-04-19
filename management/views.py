from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import ClientCategorySerializer, SampleFormSerializer, CommoditySerializer, CommodityCategorySerializer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from .custompermission import MyPermission


from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class ClientCategoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCategory.objects.all()
    serializer_class = ClientCategorySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated,MyPermission]
    
class SampleFormViewSet(viewsets.ModelViewSet):
    queryset = SampleForm.objects.all()
    serializer_class = SampleFormSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class CommodityCategoryViewSet(viewsets.ModelViewSet):
    queryset = CommodityCategory.objects.all()
    serializer_class = CommodityCategorySerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]


def Home(request):
    return redirect('api/')


             