from rest_framework import serializers
from management.models import SampleForm,SampleFormVerifier,SampleFormHasParameter,TestResult,SuperVisorSampleForm,SampleFormVerifier
from ..models import SampleTrack
from management.models import RawDataSheet,RawDataSheetDetail
from django.db.models import Q
from account.models import CustomUser


class TestResultSerializer_SampleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestResult
        fields = '__all__'

class SampleFormHasParameterSerializer_SampleTrackSerializer(serializers.ModelSerializer):
    parameter = TestResultSerializer_SampleTrackSerializer(many = True)
    class Meta:
        model = SampleFormHasParameter
        fields = '__all__'

class SuperVisorSampleFormSerializer_SampleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperVisorSampleForm
        fields = '__all__'

class SampleFormVerifierSerializer_SampleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = SampleFormVerifier
        fields = '__all__'

class CustomUserSerializer_SampleTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['get_full_name','getRoleName','role','email','username']

class SampleTrackSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer_SampleTrackSerializer()
    to_back = CustomUserSerializer_SampleTrackSerializer()
    class Meta:
        model = SampleTrack
        fields = '__all__'
    
    def to_representation(self, instance):
        representation =  super().to_representation(instance)
        if instance.form_available == "analayst":
            sampleform_has_parameter = SampleFormHasParameter.objects.filter(analyst_user_id = instance.to_back_id,sample_form_id = instance.sample_form_id).first()
            sampleform_has_parameter_serializer = SampleFormHasParameterSerializer_SampleTrackSerializer(sampleform_has_parameter).data
            representation['sampleform_has_parameter'] = sampleform_has_parameter_serializer
        
        elif instance.form_available == "supervisor":
            supervisor = SuperVisorSampleForm.objects.filter(sample_form_id = instance.sample_form_id).first()
            supervisor_sample_form_serializer = SuperVisorSampleFormSerializer_SampleTrackSerializer(supervisor).data
            representation['supervisor_sample_form'] = supervisor_sample_form_serializer
        
        elif instance.form_available == "verifier":
            verifier = SampleFormVerifier.objects.filter(sample_form_id = instance.sample_form_id).first()
            verifier_sample_form_serializer = SampleFormVerifierSerializer_SampleTrackSerializer(verifier).data
            representation['verifier_sample_form'] = verifier_sample_form_serializer

        return representation


class TrackSampleSerializer(serializers.ModelSerializer):
    track_sample = SampleTrackSerializer(many = True)
    class Meta:
        model = SampleForm
        fields = ['id','name','namuna_code','track_sample','note','remarks']

    def to_representation(self, instance):    
        representation = super().to_representation(instance)
        return representation
        

        
        
    