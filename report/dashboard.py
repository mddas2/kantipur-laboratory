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
            total_sample_forms_obj = SampleForm.objects.all()
            total_request = total_sample_forms_obj.count()
            completed = total_sample_forms_obj.filter(status = "completed").count()
            reject = total_sample_forms_obj.filter(status = "rejected").count()
            not_verified = total_sample_forms_obj.filter(verifier__is_verified = False).count()
            pending = total_sample_forms_obj.filter(status = "pending").count()
            not_assigned = total_sample_forms_obj.filter(status = "not_assigned").count()
            processing = total_sample_forms_obj.filter(status = "processing").count()

            try:
                recheck = total_sample_forms_obj.raw_datasheet.all().filter(status = "recheck").count()
                re_assigned = total_sample_forms_obj.raw_datasheet.all().filter(status = "re-assign").count()
            except:
                recheck = 1
                re_assigned = 1

            data = {
                'total_request':total_request,
                'completed':completed,
                'pending':pending,
                'not_verified':not_verified,
                "processing":processing,
                "recheck":recheck,
                "reject":reject,
                're_assigned':re_assigned,
                'not_assigned':not_assigned
            }

        elif self.request.user.role == roles.SUPERVISOR:
            total_sample_forms_obj = SampleForm.objects.filter(supervisor_user = self.request.user.id).all()
            total_request = total_sample_forms_obj.count()
            completed = total_sample_forms_obj.filter(status = "completed").count()
            reject = total_sample_forms_obj.filter(status = "rejected").count()
            not_verified = total_sample_forms_obj.filter(verifier__is_verified = False).count()
            pending = total_sample_forms_obj.filter(status = "pending").count()
            not_assigned = total_sample_forms_obj.filter(status = "not_assigned").count()
            processing = total_sample_forms_obj.filter(status = "processing").count()

            try:
                recheck = total_sample_forms_obj.raw_datasheet.all().filter(status = "recheck").count()
                re_assigned = total_sample_forms_obj.raw_datasheet.all().filter(status = "re-assign").count()
            except:
                recheck = 1
                re_assigned = 1



            data = {
                'total_request':total_request,
                'completed':completed,
                'pending':pending,
                'not_verified':not_verified,
                "processing":processing,
                "recheck":recheck,
                "reject":reject,
                're_assigned':re_assigned,
                'not_assigned':not_assigned
            }
        
        elif self.request.user.role == roles.ANALYST:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms_obj = SampleFormHasParameter.objects.filter(analyst_user = self.request.user.id).all()
            total_sample_forms = total_sample_forms_obj.count()

            pending = total_sample_forms_obj.filter(status = "pending")

            try:
                recheck = total_sample_forms_obj.raw_datasheet.all().filter(status = "recheck").count()
                re_assign = total_sample_forms_obj.raw_datasheet.all().filter(status = "re-assign").count()
            except:
                recheck = 1
                re_assign = 1

            try:
                sample_form_obj = total_sample_forms_obj.sample_form.all()
                not_verified = sample_form_obj.filter(status = "not_verified").count()
                completed = sample_form_obj.filter(status = "completed").count()
            except:
                not_verified = 1
                completed = 1

            total_report_generated = SampleFormHasParameter.objects.filter(analyst_user=self.request.user.id, sample_form__verifier__is_verified=True).count()
            data = {
                'total_request':total_sample_forms,
                'pending':pending,
                'recheck' : recheck,
                're_assign' : re_assign,
                'completed' : completed,
                'not_verified':not_verified,
            }

        elif self.request.user.role == roles.VERIFIER:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms_obj = SampleFormVerifier.objects.all()
            total_sample_forms = total_sample_forms_obj.count()
            
            not_verified = total_sample_forms_obj.filter(is_verified = False).count()
            pending = not_verified

            verified = total_sample_forms_obj.filter(is_verified=True).count()
            completed = verified

            reject = total_sample_forms_obj.filter(status = reject).count()

            data = {
                'total_request':total_sample_forms,
                'not_verified':not_verified,
                'completed':completed,
                'pending':pending,
                'reject':reject,
            }

        elif self.request.user.role == roles.USER:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms_obj = SampleForm.objects.filter(owner_user = self.request.user.email)
            total_sample_forms = total_sample_forms_obj.count()
            total_report_generated = total_sample_forms_obj.filter(verifier__is_verified=True).count()
            not_verified = total_sample_forms_obj.filter(verifier__is_verified=False).count()
            recheck = total_sample_forms_obj.filter(raw_datasheet__status="rechecks").count()
            pending = total_sample_forms_obj.filter(status = "pending").count()
            rejected = total_sample_forms_obj.filter(status = "rejected").count()
            processing = total_sample_forms_obj.filter(~Q(status = "pending") & ~Q(status="completed") ).count()
            data = {
                'total_request':total_sample_forms,
                'not_verified':not_verified,
                'processing':processing,
                'rejected':rejected,
                'completed':total_report_generated,
                'pending':pending,
                'recheck':recheck,
            }
        else:
            data = {}   

        return Response(data)