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

class TrackSampleFormAPIView(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        user = self.request.user
  
        if user.role == roles.SMU:
            return SampleForm.objects.all()
        elif user.role == roles.SUPERADMIN:
            return SampleForm.objects.all()

        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        
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