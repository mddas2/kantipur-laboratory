from django.http import HttpResponse
from rest_framework import views
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from management import roles
from account.models import CustomUser
from management.models import SampleForm,SampleFormHasParameter,SampleFormVerifier,SuperVisorSampleForm
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

            import_export = 0
            government_agencies = 0

            task_by_supervisor = []

            suspervisor_users = CustomUser.objects.filter(role = roles.SUPERVISOR)
            for supervisor_user in suspervisor_users:
                full_name = str(supervisor_user.first_name) + str(supervisor_user.last_name)
                
                supervisor_all_sample_form = supervisor_user.supervisor_sample_form.all()
                supervisor_all_sample_form_count = supervisor_all_sample_form.count()

                supervisor_completed_sample_form = supervisor_all_sample_form.filter(sample_form__status = "completed").count()
                supervisor_pending_sample_form = supervisor_all_sample_form.filter(is_supervisor_sent = False).count()
                supervisor_verifier_sent_sample_form = supervisor_all_sample_form.filter(is_supervisor_sent = True).count()
                

                data = {
                    'name':full_name,
                    'total_sample_form': supervisor_all_sample_form_count,
                    'supervisor_completed_sample_form':supervisor_completed_sample_form,
                    'supervisor_pending_sample_form':supervisor_pending_sample_form,
                    'supervisor_verifier_sent_sample_form':supervisor_verifier_sent_sample_form
                }
                task_by_supervisor.append(data)


            client_category = {
                "industry":total_request,
                "import_export":import_export,
                "government_agencies":government_agencies,
                "dftqc_section":0,
            }
            test_type_data = testTypeData(total_sample_forms_obj)
            report_generated_week = reportGeneratedWeek(total_sample_forms_obj)
            data = {
                'total_request':total_request,
                'completed':completed,
                'pending':pending,
                'not_verified':not_verified,
                "processing":processing,
                "recheck":recheck,
                "reject":reject,
                're_assigned':re_assigned,
                'not_assigned':not_assigned,
                'client_category':client_category,
                'task_by_supervisor':task_by_supervisor,
                'report_generated_week':report_generated_week,
                'test_type_data':test_type_data,
            }
            

        elif self.request.user.role == roles.SUPERVISOR:
            total_sample_forms_obj = SuperVisorSampleForm.objects.filter(supervisor_user = self.request.user.id).all()
            total_requests = total_sample_forms_obj.count()
            completed = total_sample_forms_obj.filter(sample_form__status = "completed").count()
            reject = total_sample_forms_obj.filter(sample_form__status = "rejected").count()
            not_verified = total_sample_forms_obj.filter(sample_form__verifier__is_verified = False).count()
            verified = total_sample_forms_obj.filter(sample_form__verifier__is_verified = True).count()
            pending = total_sample_forms_obj.filter(status = "pending").count()
            not_assigned = total_sample_forms_obj.filter(status = "not_assigned").count()
            processing = total_sample_forms_obj.filter(status = "processing").count()

            recheck = total_sample_forms_obj.filter(sample_form__status = "recheck").count()      

            analyst_users = CustomUser.objects.filter(role = roles.ANALYST)
            task_by_analyst = []
            for ana_user in analyst_users:
                supervisor_anaalyst_obj = ana_user.sample_has_parameter_analyst.all().filter(super_visor_sample_form__supervisor_user = request.user)
                total_request = supervisor_anaalyst_obj.count()
                name =   ana_user.email
                data = {
                    'name':name,
                    'total_request':total_request,
                }
                task_by_analyst.append(data)

            report_generated_week = reportGeneratedWeek(total_sample_forms_obj)
      
            data = {
                'total_request':total_requests,
                'completed':completed,
                'pending':pending,
                'not_verified':not_verified,
                'verified':verified,
                "processing":processing,
                "recheck":recheck,
                "reject":reject,
                'not_assigned':not_assigned,
                'task_by_analyst':task_by_analyst,
                'report_generated_week':report_generated_week,
            }
            
        
        elif self.request.user.role == roles.ANALYST:
            total_users = 0#CustomUser.objects.all().count()
            total_sample_forms_obj = SampleFormHasParameter.objects.filter(analyst_user = self.request.user.id).all()
            total_sample_forms = total_sample_forms_obj.count()

            recheck = total_sample_forms_obj.filter(status = "recheck").count()
            pending = total_sample_forms_obj.filter(status = "pending").count()
            re_assign = total_sample_forms_obj.filter(status = "re_assign").count()

    

            sample_form_obj = SampleForm.objects.filter(sample_has_parameter_analyst__analyst_user=self.request.user.id)
            not_verified = sample_form_obj.filter(status = "not_verified").count()
            completed = sample_form_obj.filter(status = "completed").count()
            

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

            try:
                reject = total_sample_forms_obj.filter(status = "rejected").count()
            except:
                reject = 1

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
            processing = total_sample_forms_obj.filter(~Q(status = "pending") & ~Q(status="completed") & ~Q(status="rejected")).count()
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

def reportGeneratedWeek(query):
    report_generated_week = []
    # Get the start and end of the current week (assuming Sunday as the start of the week)
    from django.utils import timezone
    from django.db.models import Count
    today = timezone.now()     
    start_of_week = today - timezone.timedelta(days=today.weekday())  # Sunday    
    end_of_week = start_of_week + timezone.timedelta(days=7)  # Saturday      
    # Perform the query to get the count of entries created within this week
    this_week_entries = query.filter(created_date__range=(start_of_week, end_of_week))
    # Get the count of entries for each day of the week
    counts_by_day = this_week_entries.extra({'day': 'date(created_date)'}).values('day').annotate(count=Count('id'))
    # Display the counts        
    for entry in counts_by_day:
        day = entry['day'].strftime('%A')
        count = entry['count']
        data  =  {
            "day":day,
            "count":count,
        }
        report_generated_week.append(data)
        # print(entry)
        # print(f"{entry['day'].strftime('%A')}: {entry['count']}")
    return report_generated_week

def testTypeData(query):
    chemical1 = 40
    micro1 = 35
    instrumental1 = 23
    totals = chemical1+micro1+instrumental1

    data = {
        "chemical":23,
        "micro":micro1,
        "instrumental":instrumental1,
        "total":totals
    }

    return [data]
    # chemical = SampleFormHasParameter.objects.filter(tes)
