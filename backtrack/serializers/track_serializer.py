from rest_framework import serializers
from management.models import SampleForm
from ..models import SampleTrack
from management.models import RawDataSheet

def get_user_sample_track(common_data,sample_form):
    data = {}
    data.update(common_data)
    data['user_full_name'] = "lims users"#sample_form.user.get_full_name,
    data['remarks'] = sample_form.remarks,
    return data

def get_smu_sample_track(common_data,sample_form):
    data = {}
    data.update(common_data)

    data['user_full_name'] = "lims smu"#sample_form.user.get_full_name,
    data['remarks'] = sample_form.remarks,
    return data

def get_analyst_sample_track(common_data,sample_form):
    return common_data

def get_supervisor_sample_track(common_data,sample_form):
   
    data = []
    supervisor_objs = RawDataSheet.objects.filter(sample_form = sample_form)
    supervisor_data = {}

    for sup in supervisor_objs:
        supervisor_data.update(common_data)
        supervisor_data['user_full_name'] = "lims smu"#sample_form.user.get_full_name,
        supervisor_data['remarks'] = sample_form.remarks,

        analyst_data_list = []
        for i in range(2):
            analyst_data_list.append(get_analyst_sample_track(common_data,sample_form))
        supervisor_data['analyst'] = analyst_data_list
        data.append(supervisor_data)
    return data

def get_admin_sample_track(common_data,sample_form):
    return common_data

def get_verifier_sample_track(common_data,sample_form):
    return common_data


class TrackSampleSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = SampleForm
        fields = ['id','name','namuna_code']

    def to_representation(self, instance):
        common_data = {
            'sample_id':instance.namuna_code,
            'sample_name':instance.name,
            'registered_Date':instance.created_date,
            'refrence_number':instance.refrence_number,
            'status':"pending",
        }
        print("kjhskjahd asakh kajshkj")
        representation = super().to_representation(instance)
        representation['user'] = get_user_sample_track(common_data,instance)
        representation['smu'] = get_smu_sample_track(common_data,instance)
        representation['supervisor'] = get_supervisor_sample_track(common_data,instance)
        representation['verifier'] = get_verifier_sample_track(common_data,instance)
        representation['admin'] = get_admin_sample_track(common_data,instance)
        return representation
        

        
        
    