from django.http import HttpResponse
from rest_framework import views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from management import roles
from account.models import CustomUser
from management.models import SampleForm,SampleFormHasParameter,SampleFormVerifier
from django.db.models import Q
from rest_framework.response import Response

class reportStatus(views.APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):        
        if self.request.user.role == roles.SUPERADMIN or self.request.user.role == roles.SMU:
            total_users = CustomUser.objects.all().count()
            total_sample_forms = SampleForm.objects.all().count()
            total_report_generated = SampleForm.objects.filter(verifier__is_verified=True).count()
            data = {
                'total_users':total_users,
                'total_sample_forms':total_sample_forms,
                'total_report_generated':total_report_generated,
            }

        elif self.request.user.role == roles.SUPERVISOR:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms = SampleForm.objects.filter(supervisor_user = self.request.user.id).count()
            total_report_generated = SampleForm.objects.filter(supervisor_user = self.request.user.id,verifier__is_verified=True).count()
            data = {
                'total_users':total_users,
                'total_sample_forms':total_sample_forms,
                'total_report_generated':total_report_generated,
            }
        
        elif self.request.user.role == roles.ANALYST:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms = SampleFormHasParameter.objects.filter(analyst_user = self.request.user.id).count()
            total_report_generated = SampleFormHasParameter.objects.filter(analyst_user=self.request.user.id, sample_form__verifier__is_verified=True).count()
            data = {
                'total_users':total_users,
                'total_sample_forms':total_sample_forms,
                'total_report_generated':total_report_generated,
            }

        elif self.request.user.role == roles.VERIFIER:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms = SampleFormVerifier.objects.all().count()
            total_report_generated = SampleFormVerifier.objects.filter(is_verified=True).count()
            data = {
                'total_users':total_users,
                'total_sample_forms':total_sample_forms,
                'total_report_generated':total_report_generated,
            }

        elif self.request.user.role == roles.USER:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms = SampleForm.objects.filter(owner_user = self.request.user.email).count()
            total_report_generated = SampleForm.objects.filter(verifier__is_verified=True).count()
            data = {
                'total_users':total_users,
                'total_sample_forms':total_sample_forms,
                'total_report_generated':total_report_generated,
            }
        else:
            data = {}   

        return Response(data)