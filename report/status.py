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

class GetStatus(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None):
        import json
        status = (
            ('pending', 'pending'),
            ('processing', 'processing'), 
            ('not_assigned', 'not_assigned'),
            ('not_verified', 'not_verified'),
            ('completed', 'completed'),
            ('recheck', 'recheck'),
            ('rejected', 'rejected'),
            )
        data = json.loads(status)
        return Response(data)