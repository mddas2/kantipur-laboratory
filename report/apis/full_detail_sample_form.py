from rest_framework import views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from management.encode_decode import generateDecodeIdforSampleForm
from account import roles
from management.models import SampleForm
from rest_framework.exceptions import PermissionDenied
from ..serializers_groups.full_detail_sample_form_serializers import DetailFullSampleFormSerializer

#admin level
class DetailParameterHasAssignedAnalyst(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, sample_form_id, format=None):
        sample_form_id = generateDecodeIdforSampleForm(sample_form_id,request.user)
      
        if self.request.user.role in [roles.SUPERADMIN,roles.SMU,roles.ADMIN] :#superadmin,smu
            queryset = SampleForm.objects.filter(id=sample_form_id).first()
            serializer = DetailFullSampleFormSerializer(queryset,many = False,context={'request': request})
        else:
            raise PermissionDenied("You do not have permission to access thais resource.")