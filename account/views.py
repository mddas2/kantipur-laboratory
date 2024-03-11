
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import Group, Permission
from account.models import CustomUser,UserHaveInspector
from rest_framework import viewsets
from .serializers import CustomUserRetrieveSerializer,CustomUserListSerializer,CustomUserSerializer, GroupSerializer, PermissionSerializer,RoleSerializer,departmentTypeSerializer,CustomUserReadLimitedSerializer,userAdminLevelDataSerializer,CustomUserReadAssignedSerializer,UserHaveWrirteInspectorSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken,TokenError
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account import roles
from . import department_type
from django.db.models import Q
from rest_framework import generics
from .custompermission import AccountPermission,AdminLevelPermission
from . serializers import CustomUserImageSerializer
from django.db import transaction
from .pagination import MyPageNumberPagination
from rest_framework.exceptions import PermissionDenied

from django.core.cache import cache
cache_time = 300 # 300 is 5 minute

class CustomUserSerializerViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    # permission_classes = [Account]
    serializer_class = CustomUserRetrieveSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone','department_name']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'is_recheck': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }

    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [AccountPermission]
    pagination_class = MyPageNumberPagination

    def get_permissions(self):
        if self.action == 'list':
           
            # Only allow authenticated users to list users
            return [IsAuthenticated()]
        else:
            # For other actions, no authentication is required
            return []
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CustomUserSerializer
        elif self.action in ['list']:
            return CustomUserListSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        user = self.request.user
        
        queryset = CustomUser.objects.all()
    
        if not user.is_authenticated:
            # Return an empty queryset or a default response
            query = CustomUser.objects.none()
        elif user.role == roles.SMU:  
            # query = queryset.objects.all()   
            query = queryset 
        elif user.role == roles.SUPERADMIN:
            # query = CustomUser.objects.all()    
            query = queryset       
        elif user.role == roles.ADMIN:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True)    
            query = queryset.filter(is_active = True)
        elif user.role == roles.SUPERVISOR:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True).filter(Q(role=roles.ANALYST) | Q(email = user.email))   
            query = queryset.filter(is_active = True).filter(Q(role=roles.ANALYST) | Q(email = user.email))
        elif user.role == roles.VERIFIER:
            # Regular user can see SampleForm instances with form_available='user'
            # query = CustomUser.objects.filter(is_active = True).filter(role=roles.USER)   
            query = queryset.filter(is_active = True).filter(role=roles.USER)      
        else:
            # query = CustomUser.objects.filter(email=user.email,is_active = True)
            query = queryset.filter(email=user.email,is_active = True)
            # raise PermissionDenied("You do not have permission to access this resource.")
        return query.order_by("-created_date")
     
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Save the new object to the database
        self.perform_create(serializer) #task 1

        # Create a custom response
        response_data = {
            "message": "User Account created successfully",
            "data": serializer.data
        }

        if serializer.data.get('role') == roles.INSPECTOR:
            # print(serializer.data)
            #print(serializer.data.get('id',None),"::user id")
            inspector_data = CreateInspector(serializer.data.get('id',None),request,"create")
            response_data['inspector_detail']=inspector_data
        
        name = request.POST.getlist('images[name]')
        files =  request.FILES.getlist('images[file]')
        custom_user_detail = CeateClientCategoryDetail(name,files,serializer.data['id'],"create") #task 2
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        if 'is_active' not in request.data:
            serializer.validated_data['is_active'] = instance.is_active

        if 'is_email_verified' not in request.data:
            serializer.validated_data['is_email_verified'] = instance.is_email_verified

        # Save the updated object to the database   
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "User Account updated successfully",
            "data": serializer.data
        }

        if serializer.data.get('role') == roles.INSPECTOR:
            # print(serializer.data)
            #print(serializer.data.get('id',None),"::user id")
            inspector_data = CreateInspector(serializer.data.get('id',None),request,"update")
            response_data['inspector_detail']=inspector_data

        name = request.POST.getlist('images[name]')
        files =  request.FILES.getlist('images[file]')

        custom_user_detail = CeateClientCategoryDetail(name,files,serializer.data['id'],"update")
       
        return Response(response_data)
    
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.is_active:
            # If the user is active, mark them as inactive
           
            instance.is_active = False
            instance.delete= "delete"
            instance.save()
            # Create a custom response
            response_data = {
                "message": "User Account marked as inactive"
            }
        else:
            # If the user is already inactive, return a custom error response
            response_data = {
                "message": "User Account is already inactive"
            }

        # Return the custom response
        return Response(response_data)

class RoleViewSet(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    
    def get(self,request,format=None):
        my_tuple = CustomUser.ROLE_CHOICES
        serializer = RoleSerializer(data=my_tuple,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
        # authentication_classes = [JWTAuthentication]
        # permission_classes = [IsAuthenticated]
        return Response({"roles": serialized_data},status=status.HTTP_200_OK)

class DepartmentTypesViewSet(APIView):    
    def get(self,request,format=None):
        my_tuple = department_type.department_code
        serializer = departmentTypeSerializer(data=my_tuple,many=True)
        serializer.is_valid()
        serialized_data = serializer.data
        return Response({"department_types": serialized_data},status=status.HTTP_200_OK)
     
class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Group created successfully",
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
            "message": "Group updated successfully",
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
            "message": "Group deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

    
class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name','code_name','is_verified']
    ordering_fields = ['id','name']

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

class PermissionAllDelete(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]  
    def get(self, request, format=None):
        object = Permission.objects.all().delete()
        return Response({'message': 'All permission delete successful'}, status=status.HTTP_200_OK)

class CheckTokenExpireView(APIView): 
    def get(self, request, format=None):
        # Get the token from the request headers or query parameters
        try:
            raw_token = request.META.get('HTTP_AUTHORIZATION', '').split(' ')[1]
        except:
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Verify the access token
            access_token = AccessToken(raw_token)
            access_token.verify()

            # If the token is valid and not expired
            return Response({'valid': True}, status=status.HTTP_200_OK)

        except TokenError:
            # If the token is expired or invalid
            return Response({'valid': False}, status=status.HTTP_401_UNAUTHORIZED)

    
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
            if user.is_active == False:
                return Response({'error': 'Your Account is inactive'}, status=status.HTTP_401_UNAUTHORIZED)
            login(request, user)
            refresh = RefreshToken.for_user(user)
            user_obj = CustomUserRetrieveSerializer(request.user,context={'request': request}) 
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': user_obj.data,
                'message': 'Login successful',
            }, status=status.HTTP_200_OK)

        # If the user is not authenticated, return an error message
        else:
            from django.db.models import Q
            user_obj = CustomUser.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
            if user_obj.exists():
                return Response({'error': 'Invalid password'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'error': 'Invalid username/email'}, status=status.HTTP_401_UNAUTHORIZED)

def CeateClientCategoryDetail(names,files,user_id,action):

    image_data = []

    for name, file in zip(names, files):
       dict_data = {
           'user':user_id,
           'name':name,
           'file':file,
       }
       image_data.append(dict_data)
    if len(image_data)>0:        
        image_serializer = CustomUserImageSerializer(many=True,data=image_data)
        image_serializer.is_valid(raise_exception=True)
        image_serializer.save()    
    return True

class userAssignList(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminLevelPermission]
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
        # 'test_type':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.all()
        return users

    def get_serializer_class(self):
        return CustomUserReadAssignedSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)    

class userLimitedData(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminLevelPermission]
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.filter(role = roles.USER,is_active = True)
        return users

    def get_serializer_class(self):
        return CustomUserReadLimitedSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
class userAdminLevelData(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdminLevelPermission]

    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','email','username','first_name','last_name','is_verified','phone']
    ordering_fields = ['username','id']
    filterset_fields = {
        'email': ['exact', 'icontains'],
        'username': ['exact'],
        'is_verified': ['exact'],
        'is_reject': ['exact'],
        'role': ['exact'],
        'client_category_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'is_active':['exact'],
    }
    
    def get_queryset(self):
        users = CustomUser.objects.filter(Q(role=roles.ANALYST) | Q(role = roles.SUPERVISOR) | Q(role = roles.VERIFIER) | Q(role = roles.ADMIN) | Q(role = roles.SUPERADMIN))
        return users

    def get_serializer_class(self):
        return userAdminLevelDataSerializer
    
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    

def CreateInspector(user_id,request_data,create_update):

    data = {
        'user': user_id,
        'government_id':request_data.POST.get('government_id'),
        'inspector_type':[ins_type for ins_type in request_data.POST.get('inspector_type').split(',')],
        'government_issued_document':request_data.FILES.get('government_issued_document'),
        'nepali_name':request_data.POST.get('nepali_name'),
        'branch':request_data.POST.get('branch'),
    }

    if create_update == "create":
        inspector_serializer = UserHaveWrirteInspectorSerializer(many=False,data=data,context={'request':request_data})
        inspector_serializer.is_valid(raise_exception=True)
        inspector_serializer.save() 
    else:
        inspector_obj = CustomUser.objects.get(id = user_id).inspector
        inspector_instance = UserHaveInspector.objects.get(id=inspector_obj.id)
        if request_data.FILES.get('government_issued_document') == None:
            data.pop('government_issued_document')
        inspector_serializer = UserHaveWrirteInspectorSerializer(instance=inspector_instance,data=data,context={'request':request_data})
        inspector_serializer.is_valid(raise_exception=True)
        inspector_serializer.save()
    return inspector_serializer.data


             