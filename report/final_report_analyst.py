from rest_framework import views
from management.models import SampleForm
from . analyst_final_report_serializer import CompletedSampleFormHasVerifierSerializer
from rest_framework.response import Response
from django.db.models import Q
from management import roles
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

class FinalSampleFormHasAnalystAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
      
        if user.role == roles.ANALYST:
            return SampleForm.objects.filter(Q(sample_has_parameter_analyst__status='completed') & Q(sample_has_parameter_analyst__analyst_user=user))
        else:
            return None
  
        
    def get(self, request, format=None):

        queryset = self.get_queryset()
        # print(queryset)
        # queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))

        # queryset = SampleForm.objects.all()
        serializer = CompletedSampleFormHasVerifierSerializer(queryset, many=True)
        return Response(serializer.data)