
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser
from rest_framework import viewsets
from .serializers import CustomUserSerializer, GroupSerializer, PermissionSerializer,RoleSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['email','username','is_verified']
    ordering_fields = ['username','id']
    filterset_fields = ['email','username','is_verified','role','client_category_id']
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "User Account created successfully",
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
            "message": "User Account updated successfully",
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
            "message": "User Account  deleted successfully"
        }

        # Return the custom response
        return Response(response_data)



class RoleViewSet(APIView):
    
    def get(self,request,format=None):
        my_tuple = CustomUser.ROLE_CHOICES
        serializer = RoleSerializer(data=my_tuple,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
        authentication_classes = [JWTAuthentication]
        permission_classes = [IsAuthenticated]
        return Response({"roles": serialized_data},status=status.HTTP_200_OK)
     

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    
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

    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name','code_name','is_verified']
    ordering_fields = ['id','name']

    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]    

class PermissionAllDelete(APIView):
    def get(self, request, format=None):
        object = Permission.objects.all().delete()
        return Response({'message': 'delete successful'}, status=status.HTTP_200_OK)
    
# Create your views here.
class LoginView(APIView):
    @csrf_exempt
    def post(self, request):
        username_or_email = request.data.get('email')
        password = request.data.get('password')

        # Authenticate the user using either username or email
        user = authenticate(request, username=username_or_email, password=password)
        if user is None:
            user = authenticate(request, email=username_or_email, password=password)

        # If the user is authenticated, log them in and generate tokens
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserSerializer(request.user) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            return Response({'error': 'Invalid username/email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        