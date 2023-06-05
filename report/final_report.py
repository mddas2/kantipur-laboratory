from rest_framework import views
from management.models import SampleForm
from . final_serializer import CompletedSampleFormHasVerifierSerializer
from rest_framework.response import Response

class FinalSampleFormHasVerifiedAPIView(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))

        serializer = CompletedSampleFormHasVerifierSerializer(queryset, many=True)
        return Response(serializer.data)