from rest_framework import serializers
from management.models import SampleForm

def get_user_sample_track(sample_form):
    return {}


def get_analyst_sample_track(sample_form):
    return {}

def get_supervisor_sample_track(sample_form):
    data = {
        'some':"some",
    }
    data['analyst'] = get_analyst_sample_track(sample_form)
    return data


class TrackSampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleForm
        fields = ['id','name','namuna_code']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['user'] = get_user_sample_track(instance)
        representation['smu'] = get_user_sample_track(instance)
        representation['supervisor'] = get_supervisor_sample_track(instance)
        
        
    