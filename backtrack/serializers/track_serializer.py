from rest_framework import serializers
from management.models import SampleForm

def get_user_sample_track(self,sample_form):
    a= self.common_data
    user_data = {
        'user_full_name':sample_form.user.get_full_name,
        'remarks':sample_form.remarks,
    }
    return user_data
def get_analyst_sample_track(sample_form):
    return {}

def get_supervisor_sample_track(sample_form):
    data = {
        'some':"some",
    }
    data['analyst'] = get_analyst_sample_track(sample_form)
    return data

def get_admin_sample_track(sample_form):
    return {}

def get_verifier_sample_track(sample_form):
    return {}


class TrackSampleSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, data=..., **kwargs):
        super().__init__(instance, data, **kwargs)
        self.common_data = {
            'sample_id':instance.namuna_code,
            'sample_name':instance.name,
            'registered_Date':instance.created_date,
            'refrence_number':instance.refrence_number,
            'status':"pending",
        }

    class Meta:
        model = SampleForm
        fields = ['id','name','namuna_code']

    def to_representation(self, instance):
        representation = super().to_representation(self,instance)
        representation['user'] = get_user_sample_track(self,instance)
        representation['smu'] = get_user_sample_track(self,instance)
        representation['supervisor'] = get_supervisor_sample_track(self,instance)
        representation['verifier'] = get_verifier_sample_track(self,instance)
        representation['admin'] = get_admin_sample_track(self,instance)
        return representation
        

        
        
    