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
from websocket.handle_notification import sampleFormNotificationHandler
from django.db import transaction

def BackToRole(sample_form,request,role,remarks):
    sample_form_obj = SampleForm.objects.filter(id = sample_form)
    is_update = sample_form_obj.update(is_back = back_to_status[role][-1],back_remarks = remarks)
    from_back  = request.user
    if role == roles.SMU:
        to_back = CustomUser.objects.filter(role = roles.SMU).first()
        form_available = "smu"
    elif role == roles.SUPERVISOR:
        supervisor_obj = SuperVisorSampleForm.objects.filter(sample_form_id = sample_form)
        supervisor_obj.update(is_supervisor_sent = False)
        to_back = supervisor_obj.first().supervisor_user_id
        form_available = "supervisor"
    elif role == roles.VERIFIER:
        to_back = SampleForm.objects.get(id = sample_form).verified_by_id
        form_available = "verifier"
        sample_form_obj.update(status='not_verified')
        SampleFormVerifier.objects.filter(sample_form_id = sample_form).update(is_verified = False)
        print("not verified ")
    
    data = {
        'sample_form_id':sample_form,
        'user':from_back,
        'to_back':to_back,
        'remarks':remarks,
        'status':"back",
        'form_available':form_available,
    }
    create_obj = SampleTrack.objects.create(**data)
    sampleFormNotificationHandler(create_obj,'back')
    
    return is_update
# Create your views here.
class Backto(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated,BackToPermission]

    @transaction.atomic
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