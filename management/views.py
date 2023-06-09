from django.shortcuts import render,redirect
from django.http import HttpResponse
from .serializers import MicroObservationTableSerializer,MicroParameterSerializer,ClientCategorySerializer, SampleFormWriteSerializer,SampleFormReadSerializer, CommoditySerializer, CommodityCategorySerializer, TestResultSerializer,PaymentSerializer,SuperVisorSampleFormReadSerializer,SuperVisorSampleFormWriteSerializer
from .models import ClientCategory, SampleForm, Commodity, CommodityCategory,TestResult, Payment,SuperVisorSampleForm,MicroParameter,MicroObservationTable
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .pagination import MyLimitOffsetPagination
from rest_framework.response import Response
from .custompermission import ClientCategoryPermission,SampleFormViewSetPermission,CommodityViewSetPermission,CommodityCategoryViewSetPermission,TestResultViewSetPermission,PaymentViewSetPermission
from rest_framework import status
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from . import roles
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q
from django.http import Http404
from . encode_decode import generateDecodeIdforSampleForm


class ClientCategoryViewSet(viewsets.ModelViewSet):
    queryset = ClientCategory.objects.all()
    serializer_class = ClientCategorySerializer
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name','id']
    permission_classes = [ClientCategoryPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "client category created successfully",
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
            "message": "client category updated successfully",
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
            "message": "client category deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class SuperVisorSampleFormViewset(viewsets.ModelViewSet):
    queryset = SuperVisorSampleForm.objects.all()
    serializer_class = SuperVisorSampleFormReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id']
    ordering_fields = ['id']
    filterset_fields = {
        'supervisor_user': ['exact'],
        'status': ['exact'],       
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SampleFormViewSetPermission]
    pagination_class = MyLimitOffsetPagination


    def get_queryset(self):
        user = self.request.user
        action = self.action

        print(action)
        if action == 'list':
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id,status = "not_assigned")
        elif action == 'retrieve':
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id)
        else:
            query = SuperVisorSampleForm.objects.filter(supervisor_user=user.id)

            
        if user.role == roles.SUPERVISOR:
            query =  query.filter(supervisor_user = user.id)
            # query =  SuperVisorSampleForm.objects.filter(supervisor_user = user.id)
        else:
            raise PermissionDenied("You do not have permission to access thais resource.")
        
        return query.order_by("-created_date")
        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SuperVisorSampleFormWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
    
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Add extra response data for retrieve action
        extra_data = {
            "extra_field": "Extra value for retrieve",
            "another_field": "Another value for retrieve"
        }
        # response.data.update(extra_data)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # this is for redirect for angular
        created_data = serializer.data

        sample_form_id = created_data['sample_form']
        sample_form_obj = SampleForm.objects.get(id=sample_form_id)
        all_parameters = sample_form_obj.parameters.all()

        all_supervisor_parameters = TestResult.objects.filter(supervisor_has_parameter__sample_form_id=sample_form_id)

        if all_parameters.count() == all_supervisor_parameters.count():
            total_assiged = True
        else:
            total_assiged = False

        # print(all_parameters.count(),"::",all_supervisor_parameters.count())
        # Create a custom response
        response_data = {
            "message": "submitted successfully",
            "data": serializer.data,
            "total_assiged" : total_assiged
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

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "partially updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_200_OK)
    
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
    
class SampleFormViewSet(viewsets.ModelViewSet):
    queryset = SampleForm.objects.all()
    serializer_class = SampleFormReadSerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','name','owner_user','status','form_available','commodity__name','user_refrence_number','sample_lab_id']
    ordering_fields = ['name','id']
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'owner_user': ['exact'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'supervisor_user': ['exact'],
        'created_date': ['date__gte', 'date__lte']  # Date filtering
    }
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,SampleFormViewSetPermission]
    pagination_class = MyLimitOffsetPagination

    def get_object(self):
        user = self.request.user

        id = generateDecodeIdforSampleForm(self.kwargs['pk'],user) 
    
        queryset = self.get_queryset()
        obj = queryset.filter(id=id).first()
        if not obj:
            raise Http404("Object not found")

        return obj

    def get_queryset(self):
        user = self.request.user

        if user.role == roles.USER:         
            query =  SampleForm.objects.filter(Q(owner_user = user.email) & ~Q(status="completed") )
        elif user.role == roles.SUPERVISOR:
            query =  SampleForm.objects.filter(supervisor_user=user,status="not_assigned")
            if self.request.method == "PATCH":
                query =  SampleForm.objects.filter(supervisor_user=user)
        elif user.role == roles.SMU:
            query = SampleForm.objects.filter(Q(form_available = 'smu') or Q(status = "not_assigned")).filter(~Q(status = "rejected"))
        elif user.role == roles.SUPERADMIN:
            query = SampleForm.objects.filter(Q(form_available = 'smu') or Q(status = "not_assigned")).filter(~Q(status = "rejected"))
        elif user.role == roles.ADMIN:
            query = SampleForm.objects.filter(status = "not_approved")
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        
        return query.order_by("-created_date")
        
        
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return SampleFormWriteSerializer
        return super().get_serializer_class()
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
    
        return response

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        
        # Add extra response data for retrieve action
        extra_data = {
            "extra_field": "Extra value for retrieve",
            "another_field": "Another value for retrieve"
        }
        # response.data.update(extra_data)
        return response
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "Sample submitted successfully",
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
            "message": "Sample updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        print(instance.id)
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        # Save the updated object to the database
        self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "Sample partially updated successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_200_OK)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        # Perform the default delete logic
        self.perform_destroy(instance)

        # Create a custom response
        response_data = {
            "message": "Sample deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
    
class CommodityViewSet(viewsets.ModelViewSet):
    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer   
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['name','id']
    search_fields = ['name']
    filterset_fields = ['name','category_id']
    # authentication_classes = [JWTAuthentication]
    permission_classes = [CommodityViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "commodity created successfully",
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
            "message": "commodity updated successfully",
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
            "message": "commodity deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
class CommodityCategoryViewSet(viewsets.ModelViewSet):

    queryset = CommodityCategory.objects.all()
    serializer_class = CommodityCategorySerializer
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    filterset_fields = ['name','id']
    search_fields = ['name']
    # authentication_classes = [JWTAuthentication]
    permission_classes = [CommodityCategoryViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "commodity category created successfully",
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
            "message": "commodity category updated successfully",
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
            "message": "commodity category deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class TestResultViewSet(viewsets.ModelViewSet):
    queryset = TestResult.objects.all()
    serializer_class = TestResultSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name','formula']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,TestResultViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "parameter created successfully",
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
            "message": "parameter updated successfully",
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
            "message": "parameter deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class PaymentViewSet(viewsets.ModelViewSet):
    from rest_framework.parsers import MultiPartParser, FormParser
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,PaymentViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    
    parser_classes = [MultiPartParser, FormParser]


    
    def create(self, request, *args, **kwargs):
        payment_dict = {}
        for key, value in request.data.items():
            if key.startswith('payments'):
                start_index = key.index('[')
                end_index = key.index(']')
                index = key[start_index + 1:end_index]
                field = key[end_index + 2:-1]  # Adjust the index according to the key format

                if index not in payment_dict:
                    payment_dict[index] = {}

                payment_dict[index][field] = value

        payment_data = []

        for index, payment_data_dict in payment_dict.items():
            serializer = PaymentSerializer(data=payment_data_dict)
            serializer.is_valid(raise_exception=True)
            payment_obj = serializer.save()
            payment_data.append(serializer.data)

        response_data = {
            "message": "Payments created successfully",
            "data": payment_data
        }

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
            "message": "payment updated successfully",
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
            "message": "payment deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

class MicroparameterViewset(viewsets.ModelViewSet):
    queryset = MicroParameter.objects.all()
    serializer_class = MicroParameterSerializer   
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['id']
    filterset_fields = ['id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,CommodityViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "MicroparameterViewset created successfully",
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
            "message": "MicroparameterViewset updated successfully",
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
            "message": "MicroparameterViewset deleted successfully"
        }

        # Return the custom response
        return Response(response_data)
    
class MicroObservationTableViewSet(viewsets.ModelViewSet):
    queryset = MicroObservationTable.objects.all()
    serializer_class = MicroObservationTableSerializer   
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    ordering_fields = ['id']
    search_fields = ['id']
    filterset_fields = ['id']
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,CommodityViewSetPermission]
    pagination_class = MyLimitOffsetPagination
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data,many=True)
        serializer.is_valid(raise_exception=True)

        # Save the new object to the database
        self.perform_create(serializer)

        # Create a custom response
        response_data = {
            "message": "MicroObservationTable created successfully",
            "data": serializer.data
        }

        # Return the custom response
        return Response(response_data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        
        data = request.data
        for dat in data:
            print(dat)
            # update_url_id = dat.ids
            print(dat)
            partial = kwargs.pop('partial', False)
            instance = MicroObservationTable.objects.get(id = dat['id'])
            serializer = self.get_serializer(instance, data=dat, partial=partial)
            serializer.is_valid(raise_exception=True)

            # Save the updated object to the database
            self.perform_update(serializer)

        # Create a custom response
        response_data = {
            "message": "MicroObservationTable updated successfully",
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
            "message": "MicroObservationTable deleted successfully"
        }

        # Return the custom response
        return Response(response_data)

    
def Home(request):
    from account.models import CustomUser
    from management.models import ClientCategory
    clien_category = ClientCategory.objects.get(id='1')
    user = CustomUser.objects.get(id='1')
    user.client_category = clien_category
    user.save()
    return HttpResponse(user)
   


             