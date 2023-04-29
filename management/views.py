from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import ClientCategorySerializer, SampleFormSerializer, CommoditySerializer, CommodityCategorySerializer, TestResultSerializer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination

from .custompermission import MyPermission


class ClientCategoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCategory.objects.all()
    serializer_class = ClientCategorySerializer
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated,MyPermission]
    pagination_class = MyLimitOffsetPagination
    
class SampleFormViewSet(viewsets.ModelViewSet):
    queryset = SampleForm.objects.all()
    serializer_class = SampleFormSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyLimitOffsetPagination
    
    
class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyLimitOffsetPagination
    
class CommodityCategoryViewSet(viewsets.ModelViewSet):
    queryset = CommodityCategory.objects.all()
    serializer_class = CommodityCategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyLimitOffsetPagination

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = CommodityCategory.objects.all()
    serializer_class = TestResultSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = MyLimitOffsetPagination
    
def Home(request):
    from account.models import CustomUser
    from management.models import ClientCategory
    clien_category = ClientCategory.objects.get(id='1')
    user = CustomUser.objects.get(id='1')
    user.client_category = clien_category
    user.save()
    return HttpResponse(user)
    return redirect('api/')


             