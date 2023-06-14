from rest_framework import views
from management.models import SampleForm
from . final_serializer import CompletedSampleFormHasVerifierSerializer
from . analyst_final_report_serializer import CompletedSampleFormHasAnalystSerializer
from rest_framework.response import Response
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class FinalSampleFormHasVerifiedAPIView(views.APIView):
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

    def get_queryset(self):
        user = self.request.user
  
        if user.role == roles.USER:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True) & Q(owner_user=user.email))
        elif user.role == roles.SUPERVISOR:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True) & Q(supervisor_user=user))
        elif user.role == roles.SMU:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True))
        elif user.role == roles.SUPERADMIN:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True))
        elif user.role == roles.ANALYST:
            query = SampleForm.objects.filter(Q(sample_has_parameter_analyst__status='completed') & Q(sample_has_parameter_analyst__analyst_user=user) & Q(sample_has_parameter_analyst__is_supervisor_sent=True))
        elif user.role == roles.VERIFIER:
            query = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=True))
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        return query.order_by("-created_date")
        
    def get(self, request, format=None):

        queryset = self.get_queryset()
        # print(queryset)
        # queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))

        # queryset = SampleForm.objects.all()
        if self.request.user.role == roles.ANALYST:
            serializer = CompletedSampleFormHasAnalystSerializer(queryset, many=True)
        else:
            serializer = CompletedSampleFormHasVerifierSerializer(queryset, many=True)
        return Response(serializer.data)