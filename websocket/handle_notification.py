from account.models import CustomUser
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting
from . import mapping_notification_type
from account import roles
from django.db.models import Q
from management import encode_decode
from django.contrib.contenttypes.models import ContentType
from backtrack.models import SampleTrack
from management.models import SuperVisorSampleForm

def NotificationHandler(instance,notification_type):
        
    if notification_type == "create_user":
        notification_message =  f"A new user <strong>{instance.get_full_name}</strong> has submitted an account for verification."
        particular_message =  '.'

        to_notification = CustomUser.objects.filter(role = roles.SMU)
        to_notification = to_notification.values_list('id', flat=True)

        from_notification = instance.id
        print(instance.id)
        path = "dashboard/user-details/" + str(instance.id)

    elif notification_type == "recheck":
        notification_message =  f"Your account is sent back to you for recheck."
        particular_message =  '.'

        from_notification = CustomUser.objects.filter(role = roles.SMU).first().id

        to_notification = [instance.id]
        path = "dashboard/user-details/" + str(instance.id)
    
    # Create notification data
    notification_data = {
        "notification_message": notification_message,
        'particular_message':particular_message,
        "path": path,
        "from_notification": from_notification,
        "is_read": False,
        "to_notification": to_notification,
        'method_type':notification_type,

        'object_id':instance.id,
        'model_type':notification_type,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
    }

    print('----------------hello---------------')
    # Serialize the notification data
    serializer = NotificationWriteSerializer(data=notification_data)
    serializer.is_valid(raise_exception=True)

    # Save the new notification object
    notification = serializer.save()

    # Create a custom response
    response_data = {
        "message": "Notification created successfully",
        "data": serializer.data
    }

    # to_email = CustomUser.objects.values_list('email', flat=True)
    # ESendMail(notification_message,to_email)
    return response_data, status.HTTP_201_CREATED

def sampleFormNotificationHandler(instance,notification_type):
    # from_notification = mapping_notification_type.mapping[notification_type]['from_user']
    print("notification create::",notification_type)

    create_track_obj = True
    is_notification = True
    if notification_type == 'back':
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        to_back_role = instance.to_back.role

        print("notification handling path::",to_back_role)
        if to_back_role == roles.SMU:
            path = '/dashboard/sample-assigned-details/'+str(instance.sample_form.id)
        elif to_back_role == roles.SUPERVISOR:
            path = "/dashboard/sample-report/" + str(SuperVisorSampleForm.objects.filter(sample_form_id = instance.sample_form_id).first().id)
        elif to_back_role == roles.VERIFIER:
            path =  "/dashboard/verify-sample-report/" + str(instance.sample_form.sample_lab_id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,role=instance.user.getRoleName)

        to_notification = [instance.to_back_id]
        from_notification = instance.user_id
        create_track_obj = False
        sample_form_id_for_track = instance.sample_form
        #store in back track model SampleTrack
    elif notification_type == 'submit_back':
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = "/dashboard/verify-sample-report/" + str(instance.sample_form.sample_lab_id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code)

        to_notification = [instance.to_back_id]
        from_notification = instance.user_id
        create_track_obj = False
        sample_form_id_for_track = instance.sample_form

    elif notification_type == "sample_initialized":
        #SampleTrack
        notification_type = "new_sample_form"
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)
        if instance.client_category_detail.client_category_id == 12:
            path = path + '?type=formal'     
        notification_message =  notification_message.format(sample_name = instance.name,namuna_code = instance.namuna_code,first_name = instance.owner_user_obj.first_name ,last_name = instance.owner_user_obj.last_name)
        refrence_number = encode_decode.generateEncodeIdforSampleForm(instance.id, "user")
        particular_message =  particular_message.format(refrence_number = refrence_number)

        to_notification = CustomUser.objects.filter(role = roles.SMU)
        to_notification = to_notification.values_list('id', flat=True)

        from_notification = instance.owner_user_obj_id
        form_available = "smu"
        sample_form_id_for_track = instance
        is_notification = False
        notification_type = "sample_initialized"

        remarks =  instance.note

    elif notification_type == "new_sample_form":
        #SampleTrack
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)
        if instance.client_category_detail.client_category_id == 12:
            path = path + '?type=formal'     
        notification_message =  notification_message.format(sample_name = instance.name,namuna_code = instance.namuna_code,first_name = instance.owner_user_obj.first_name ,last_name = instance.owner_user_obj.last_name)
        refrence_number = encode_decode.generateEncodeIdforSampleForm(instance.id, "user")
        particular_message =  particular_message.format(refrence_number = refrence_number)

        to_notification = CustomUser.objects.filter(role = roles.SMU)
        to_notification = to_notification.values_list('id', flat=True)

        from_notification = instance.owner_user_obj_id
        form_available = "smu"
        sample_form_id_for_track = instance
        remarks =  ''
    
    if notification_type == "recheck_sample":
        #SampleTrack
        print(" recheck sample inside")
        instance = instance.first()
        print(instance.id)
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)
        
        notification_message =  notification_message.format(sample_name = instance.name)
        # refrence_number = encode_decode.generateEncodeIdforSampleForm(instance.id, "user")
        particular_message =  '.'

        to_notification = [instance.owner_user_obj_id]
        from_notification = CustomUser.objects.filter(role = roles.SMU).first().id
        form_available = "smu"
        sample_form_id_for_track = instance

        remarks =  instance.remarks
   
    elif notification_type == "assigned_supervisor":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,smu_first_name = CustomUser.objects.filter(role = roles.SMU).first().first_name,smu_last_name = CustomUser.objects.filter(role = roles.SMU).first().last_name)
        to_notification = [instance.supervisor_user_id]  # here instance is supervisoruser

        from_notification = CustomUser.objects.filter(role = roles.SMU).first().id
        form_available = "supervisor"
        sample_form_id_for_track = instance.sample_form
        remarks =  ''

    elif notification_type == "assigned_analyst":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,supervisor_first_name=instance.super_visor_sample_form.supervisor_user.first_name,supervisor_last_name=instance.super_visor_sample_form.supervisor_user.last_name)

        to_notification = [instance.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.super_visor_sample_form.supervisor_user_id
        form_available = "analayst"
        sample_form_id_for_track = instance.sample_form
        remarks =  ''

    elif notification_type == "sent_to_supervisor":

        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']

        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.super_visor_sample_form_id)
        if instance.sample_form.client_category_detail.client_category_id == 12:
            path = path + '?type=formal'       

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,analyst_first_name = instance.analyst_user.first_name,analyst_last_name=instance.analyst_user.last_name)
        to_notification = [instance.super_visor_sample_form.supervisor_user_id]#[instance.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.analyst_user_id
        form_available = "supervisor"
        sample_form_id_for_track = instance.sample_form
        remarks =  instance.remarks
    
    elif notification_type == "parameter_recheck":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.sample_form_has_parameter_id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,supervisor_first_name=instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user.first_name,supervisor_last_name=instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user.last_name)
        to_notification = [instance.sample_form_has_parameter.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user_id
        form_available = "analyst"
        sample_form_id_for_track = instance.sample_form
        remarks =  instance.remarks

    elif notification_type == "assigned_verifier":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path']+str(instance.sample_form.sample_lab_id)
        
        supervisor_obj = instance.sample_form.supervisor_sample_form.all().first().supervisor_user
        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code , supervisor_first_name = supervisor_obj.first_name,supervisor_last_name = supervisor_obj.last_name)

        to_notification = CustomUser.objects.filter(role = roles.VERIFIER)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification = instance.sample_form.supervisor_sample_form.first().supervisor_user_id
        form_available = "verifier"
        sample_form_id_for_track = instance.sample_form
        remarks =  instance.remarks

    elif notification_type == "assigned_admin":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.sample_form.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,verified_by_first_name = instance.sample_form.verified_by.first_name,verified_by_last_name = instance.sample_form.verified_by.last_name)

        to_notification = CustomUser.objects.filter(role = roles.ADMIN)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification =CustomUser.objects.filter(role = roles.VERIFIER).first().id
        form_available = "admin"
        sample_form_id_for_track = instance
        remarks =  instance.remarks

    elif notification_type == "approved_sample_form":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = "/dashboard/sample-test-report/"+str(instance.refrence_number)
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)
        # dashboard/sample-test-report/J1AkLj #user path
        notification_message = notification_message.format(sample_name = instance.name,namuna_code = instance.namuna_code)
        if instance.client_category_detail.client_category_id == 12:
            to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(role = roles.SUPERADMIN) | Q(id = instance.owner_user_obj_id))
        else:
            to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(role = roles.VERIFIER) | Q(role = roles.SUPERADMIN) | Q(id = instance.owner_user_obj_id))
        to_notification = to_notification.values_list('id', flat=True)

        from_notification =CustomUser.objects.filter(role = roles.ADMIN).first().id
        form_available = "admin"
        sample_form_id_for_track = instance
        remarks =  instance.remarks

    if create_track_obj == True:
        track_data = {
            'sample_form_id':sample_form_id_for_track.id,
            'user_id':from_notification,
            'to_back_id':to_notification[0],
            'remarks':remarks,
            'description':notification_message,
            'status':notification_type,
            'form_available':form_available
        }
        create_obj = SampleTrack.objects.create(**track_data) #this data is for model sample track
        print(create_obj," reassigned sample")

    notification_data = {
        "notification_message": notification_message,
        'particular_message':particular_message,
        "path": path,
        "from_notification": from_notification,
        "is_read": False,
        "to_notification": to_notification,
        'method_type':notification_type,

        'object_id':instance.id,
        'model_type':notification_type,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
    }
    # print(notification_data)
    # return True

    # Serialize the notification data
    serializer = NotificationWriteSerializer(data=notification_data)
    serializer.is_valid(raise_exception=True)

    if is_notification:
        # Save the new notification object
        notification = serializer.save()
        # Create a custom response
        response_data = {
            "message": "sample form Notification created successfully ",
            "data": serializer.data,
        }
        return response_data, status.HTTP_201_CREATED
    
    else:
        response_data = {
            "message": "sample form Notification created successfully ",
            "data": "",
        }
        return response_data, status.HTTP_201_CREATED




    