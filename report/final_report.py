from rest_framework import views
from management.models import SampleForm
from . final_serializer import CompletedSampleFormHasVerifierSerializer
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
        print(user)

        if user.role == roles.USER:
            return SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False) & Q(owner_user=user.email))
            return SampleForm.objects.filter(owner_user = user.email)
        elif user.role == roles.SUPERVISOR:
            # Admin can see SampleForm instances with form_available='admin'
            return SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False) & Q(supervisor_user=user))
            return SampleForm.objects.filter(supervisor_user = user)
        elif user.role == roles.SMU:
            return SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))
            return SampleForm.objects.all()
        elif user.role == roles.SUPERADMIN:
            return SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))
            # Regular user can see SampleForm instances with form_available='user'
            return SampleForm.objects.all()
        else:
            raise PermissionDenied("You do not have permission to access this resource.")
        
    def get(self, request, format=None):

        queryset = self.get_queryset()

        # queryset = SampleForm.objects.filter(Q(verifier__is_sent=True) & Q(verifier__is_verified=False))

        # queryset = SampleForm.objects.all()
        serializer = CompletedSampleFormHasVerifierSerializer(queryset, many=True)
        return Response(serializer.data)