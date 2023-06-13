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

class FinalSampleFormHasVerifiedAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
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
        return query.latest('created_date')
        
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