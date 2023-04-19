from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import ClientCategorySerializer, SampleFormSerializer, CommoditySerializer, CommodityCategorySerializer,CustomUserSerializer
from .serializers import ClientCategorySerializer, SampleFormSerializer, CommoditySerializer, CommodityCategorySerializer,CustomUserSerializer, GroupSerializer, PermissionSerializer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import Group, Permission

from .custompermission import MyPermission
from account.models import CustomUser

from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

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
    

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]
    
    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]    


class PermissionAllDelete(APIView):
    def get(self, request, format=None):
        object = Permission.objects.all().delete()
        serializer_class = PermissionSerializer
        return Response({'detail': 'delete successful'}, status=status.HTTP_200_OK)


def Home(request):
    return redirect('api/')


             