
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser
from rest_framework import viewsets
from .serializers import CustomUserSerializer, GroupSerializer, PermissionSerializer
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # authentication_classes = [SessionAuthentication]
    # permission_classes = [IsAuthenticated]

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
# Create your views here.
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