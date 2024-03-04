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
    search_fields = ['id','namuna_code','code','name','owner_user_obj__name','status','form_available','commodity__name']
    ordering_fields = ['name','id']
    
    filterset_fields = {
        'name': ['exact', 'icontains'],
        'status': ['exact'],
        'form_available': ['exact'],
        'commodity_id': ['exact'],
        'created_date': ['date__gte', 'date__lte'],  # Date filtering
        'client_category_detail__client_category':['exact'],
    }

    def get_queryset(self):
        user = self.request.user 
<<<<<<< HEAD
        query = SampleForm.objects.filter(Q(status="processing") | Q(status="not_verified"))
        return query.order_by("-supervisor_sample_form__created_date")
=======
       
        if user.role in [roles.SMU,roles.SUPERADMIN]:
            query = SampleForm.objects.filter(Q(status="processing") | Q(status="not_verified") | Q(status="not_approved"))
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        return query.order_by("-created_date")
>>>>>>> main
    
    def get_serializer_class(self):
        if self.request.user.role == roles.SMU or self.request.user.role == roles.SUPERADMIN:
            serializer = AssignedSampleForSmuSuperAdminSerializer
        return serializer
        
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)