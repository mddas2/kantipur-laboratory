from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import ClientCategorySerializer, SampleFormSerializer, CommoditySerializer, CommodityCategorySerializer,CustomUserSerializer,LoginSerializer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt

from .custompermission import MyPermission
from account.models import CustomUser

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

def Home(request):
    return redirect('api/')

class LoginView(APIView):
    @csrf_exempt
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                print(request)
                return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
             