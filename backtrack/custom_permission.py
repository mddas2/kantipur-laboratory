from rest_framework.permissions import BasePermission
from management.models import SampleForm
from management.encode_decode import generateDecodeIdByRoleforSampleForm
from .back_track_status import role_track_mapping
from backtrack.models import SampleTrack
from account import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def VerifyOwner(request,sample_form,role):
    # print(role_track_mapping)
    verify = role_track_mapping.get(f'{role}-{request.user.role}',[None,None,False])
    if verify[-1]:
        print(request.user.role," to " , role, '\n', 'sample_form_status:' ,SampleForm.objects.get(id = sample_form).status," matpped_data",verify)
        sample_obj = SampleForm.objects.get(id = sample_form)
        if verify[1] == sample_obj.status:
            return True
            # track_sample = sample_obj.track_sample.all()
            # print(track_sample, " track sample ")
            # if track_sample.exists():
            #     if track_sample.last().status != 'back':
            #         return True
            #     else:
            #         return False
            # else:
            #     return True
        return False
    return False   

def TrackLevel(request,sample_form,role):
    return bool(IsAuthenticated(request) and request.user.role in [roles.SMU,roles.SUPERVISOR,roles.VERIFIER,roles.ADMIN] and VerifyOwner(request,sample_form,role))

class BackToPermission(BasePermission):
    def has_permission(self, request, view):
        
        role = view.kwargs.get('role')
        sample_form = view.kwargs.get('sample_form')
        sample_form = generateDecodeIdByRoleforSampleForm(sample_form,request.user.role)
        if request.method == 'POST':
            return TrackLevel(request,sample_form,role)
        else:
            False
            