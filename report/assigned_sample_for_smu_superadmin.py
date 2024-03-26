from management.models import SampleForm
from . final_serializer import AssignedSampleForSmuSuperAdminSerializer

from django.db.models import Q
from account import roles
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .custompermission import AdmnLevelPermission
from .pagination import MyPageNumberPaginatiton

class AssignedSampleForSmuSuperAdmin(generics.ListAPIView):
 
    authentication_classes = [JWTAuthentication]
    permission_classes = [AdmnLevelPermission]
    pagination_class = MyPageNumberPaginatiton
  
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['id','namuna_code','code','name','owner_user_obj__first_name','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'client_category_detail__client_category':['exact'],
        'is_back':['exact','icontains']
    }

    def get_queryset(self):
        query = SampleForm.objects.filter(Q(status="processing") | Q(status="not_verified"))
        return query.order_by("-supervisor_sample_form__created_date")#.order_by("is_back")
    
    def get_serializer_class(self):
        if self.request.user.role == roles.SMU or self.request.user.role == roles.SUPERADMIN:
            serializer = AssignedSampleForSmuSuperAdminSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)