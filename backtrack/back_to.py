from django.shortcuts import render
from rest_framework import views
from management.models import SampleForm
from .serializers.track_serializer import TrackSampleSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from .custom_permission import BackToPermission
from management.encode_decode import generateDecodeIdByRoleforSampleForm
from rest_framework import status
from .back_track_status import role_track_mapping,back_to_status
from account import roles
from management.models import SuperVisorSampleForm,SampleFormVerifier
from .models import SampleTrack
from account.models import CustomUser

def BackToRole(sample_form,request,role,remarks):
    is_update = SampleForm.objects.filter(id = sample_form).update(is_back = back_to_status[role][-1],back_remarks = remarks)
    from_back  = request.user
    if role == roles.SMU:
        to_back = CustomUser.objects.filter(role = roles.SMU).first()
        form_available = "SMU"
    elif role == roles.SUPERVISOR:
        supervisor_obj = SuperVisorSampleForm.objects.filter(sample_form_id = sample_form)
        supervisor_obj.update(is_supervisor_sent = False)
        to_back = supervisor_obj.first().supervisor_user_id
        form_available = "SUPERVISOR"
    elif role == roles.VERIFIER:
        to_back = SampleForm.objects.get(id = sample_form).verified_by_id
        form_available = "VERIFIER"
    
    #create_obj = SampleTrack.objects.create(user = from_back,to_back = to_back, remarks = remarks,status = 'back',form_available = form_available)
    
    return is_update
# Create your views here.
class Backto(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,BackToPermission]
    def post(self, request, role, sample_form, format=None):
        sample_form = generateDecodeIdByRoleforSampleForm(sample_form,request.user.role)
        remarks = request.data.get('back_remarks')
        print(remarks)
        is_back = BackToRole(sample_form,request,role,remarks)
        if is_back:
            data  = {
                "message":f"sample Back to {role} is successfully."
            }
            return Response(data,status=status.HTTP_200_OK)
        else:
            data  = {
                "message":f"Fail to send back sample."
            }
            return Response(data,status=status.HTTP_400_BAD_REQUEST)