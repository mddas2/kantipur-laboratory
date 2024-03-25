from rest_framework import serializers
from management.models import SampleForm,SampleFormVerifier
from ..models import SampleTrack
from management.models import RawDataSheet,RawDataSheetDetail

def get_user_sample_track(common_data,sample_form):
    data = {
        'user_full_name': sample_form.owner_user_obj.get_full_name,
        'remarks':sample_form.remarks,
    }
    data.update(common_data)
    data['status'] = "pending"
    return data

def get_smu_sample_track(common_data,sample_form):
    
    data = {
        'user_full_name':sample_form.smu.get_full_name,
        'remarks':sample_form.remarks
    }
    data.update(common_data)
    return data

def get_analyst_sample_track(common_data,sample_form):
    # return common_data
    analyst_data_list = []
    analyst_data =  {}
    rawdatasheets = RawDataSheet.objects.filter(sample_form = sample_form)
    for raw_data in rawdatasheets:
        parameters_raw_datas  = RawDataSheetDetail.objects.filter(raw_data = raw_data)
        for param in parameters_raw_datas:
            analyst_data = {
                'user_full_name':raw_data.sample_form_has_parameter.analyst_user.get_full_name,
                'status':raw_data.status,
                'refrence_number':common_data.get('refrence_number'),
                'registered_Date':common_data.get('created_date'),
                "registered_Date":common_data.get('created_date')
            }
            print(raw_data.status)
            # analyst_data.update(common_data)s
            analyst_data['status'] = raw_data.status
            analyst_data_list.append(analyst_data)
    return analyst_data_list


def get_supervisor_sample_track(common_data,sample_form):
   
    data = []
    supervisor_objs = RawDataSheet.objects.filter(sample_form = sample_form)
    

    for sup in supervisor_objs:
        
        supervisor_data = {}
        
        analyst_data_list = get_analyst_sample_track(common_data,sample_form)
    
        supervisor_data = {
            'user_full_name':sample_form.supervisor_sample_form.all().first().supervisor_user.get_full_name,
            'remarks':sample_form.remarks,
            'analyst':analyst_data_list
        }
        supervisor_data.update(common_data)
        data.append(supervisor_data)
     
    return data

def get_admin_sample_track(common_data,sample_form):
        return common_data
        if sample_form.status == "completed":
            data = {
                'sample_id':sample_form.sample_lab_id,
                'sample_name':sample_form.name,
                'register_date':sample_form.created_date,
                'refrence_number':sample_form.refrence_number,
                'status':"completed",
            }
            return data
        else:
            return common_data

def get_verifier_sample_track(common_data,sample_form):
    verifier_obj = SampleFormVerifier.objects.filter(sample_form = sample_form.id)
    
    if verifier_obj.exists():
        data = {
            'sample_id':sample_form.sample_lab_id,
            'sample_name':sample_form.name,
            'register_date':sample_form.created_date,
            'refrence_number':sample_form.refrence_number,
            'status':sample_form.status

        }
        return data
    
        
        


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
            'status':instance.status,
        }
    
        representation = super().to_representation(instance)
        representation['user'] = get_user_sample_track(common_data,instance)
        representation['smu'] = get_smu_sample_track(common_data,instance)
        representation['supervisor'] = get_supervisor_sample_track(common_data,instance)
        representation['verifier'] = get_verifier_sample_track(common_data,instance)
        representation['admin'] = get_admin_sample_track(common_data,instance)
        return representation
        

        
        
    