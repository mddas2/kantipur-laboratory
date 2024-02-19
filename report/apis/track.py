from management.models import SampleForm
from ..serializers_groups.track_serializers import TrackSampleFormSerializer

from account import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from ..pagination import MyPageNumberPaginatiton

class TrackSampleFormAPIView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,DjangoFilterBackend,OrderingFilter]
    search_fields = ['name','owner_user','status','form_available','commodity__name']
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
    pagination_class = MyPageNumberPaginatiton
    def get_queryset(self):
        user = self.request.user
  
        if user.role == roles.SMU:
            query = SampleForm.objects.all()
        elif user.role == roles.SUPERADMIN:
            query = SampleForm.objects.all()
        elif user.role == roles.ADMIN:
            query = SampleForm.objects.all()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
    
        return query.order_by("-created_date")
    
    def get_serializer_class(self):
        return TrackSampleFormSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    