from account.models import CustomUser
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting
from . import mapping_notification_type
from account import roles
from django.db.models import Q
from management import encode_decode
from django.contrib.contenttypes.models import ContentType

def NotificationHandler(instance, request,method,model_name):
    # return True
    to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(id = instance.id))
    
    to_notification = to_notification.values_list('id',flat=True)
    notification_type = ""
    if method == "update":
        notification_type = "customuser_update"
        notification_message = "User "+str(instance.username) + " has been modified"
        particular_message = "Your aaccount has been modified"
    elif method == "create":
        notification_type = "customuser_create"
        notification_message= f"New user ({str(instance.username)}) has registered an account."
        particular_message = "Your account has been created successfully"
    path = frontend_setting.particular_user + str(instance.id)
    try:
        from_notification = request.user.id
    except:
        from_notification = instance.id

    model_name = "CustomUser"    

    # Create notification data
    notification_data = {
        "notification_message": notification_message,
        'particular_message':particular_message,
        "path": path,
        "from_notification": from_notification,
        "is_read": False,
        "to_notification": to_notification,
        'method_type':model_name,

        'object_id':instance.id,
        'content_object':instance,
        'content_type':ContentType.objects.get_for_model(instance).id,
    }

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
    if notification_type == 'is_back':
        print("creating is_back notification")
        pass
        #store in back track model SampleTrack
    elif notification_type == 'submit_back':
        pass
        #store in back track model
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
   
    elif notification_type == "assigned_supervisor":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,smu_first_name = CustomUser.objects.filter(role = roles.SMU).first().first_name,smu_last_name = CustomUser.objects.filter(role = roles.SMU).first().last_name)
        to_notification = [instance.supervisor_user_id]  # here instance is supervisoruser

        from_notification = CustomUser.objects.filter(role = roles.SMU).first().id

    elif notification_type == "assigned_analyst":
        print(" re- assigned analyst ")
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,supervisor_first_name=instance.super_visor_sample_form.supervisor_user.first_name,supervisor_last_name=instance.super_visor_sample_form.supervisor_user.last_name)

        to_notification = [instance.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.super_visor_sample_form.supervisor_user_id

    elif notification_type == "sent_to_supervisor":

        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']

        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.super_visor_sample_form_id)
        if instance.sample_form.client_category_detail.client_category_id == 12:
            path = path + '?type=formal'       

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,analyst_first_name = instance.analyst_user.first_name,analyst_last_name=instance.analyst_user.last_name)
        to_notification = [instance.super_visor_sample_form.supervisor_user_id]#[instance.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.analyst_user_id
    
    elif notification_type == "parameter_recheck":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.sample_form_has_parameter_id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,supervisor_first_name=instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user.first_name,supervisor_last_name=instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user.last_name)
        to_notification = [instance.sample_form_has_parameter.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.sample_form_has_parameter.super_visor_sample_form.supervisor_user_id

    elif notification_type == "assigned_verifier":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path']+str(instance.sample_form.sample_lab_id)
        
        supervisor_obj = instance.sample_form.supervisor_sample_form.all().first().supervisor_user
        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code , supervisor_first_name = supervisor_obj.first_name,supervisor_last_name = supervisor_obj.last_name)

        to_notification = CustomUser.objects.filter(role = roles.VERIFIER)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification = instance.sample_form.supervisor_sample_form.first().supervisor_user_id

    elif notification_type == "assigned_admin":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.sample_form.id)

        notification_message = notification_message.format(sample_name = instance.sample_form.name,namuna_code = instance.sample_form.namuna_code,verified_by_first_name = instance.sample_form.verified_by.first_name,verified_by_last_name = instance.sample_form.verified_by.last_name)

        to_notification = CustomUser.objects.filter(role = roles.ADMIN)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification =CustomUser.objects.filter(role = roles.VERIFIER).first().id

    elif notification_type == "approved_sample_form":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)
        # dashboard/sample-test-report/J1AkLj #user path

        notification_message = notification_message.format(sample_name = instance.name,namuna_code = instance.namuna_code)
        if instance.client_category_detail.client_category_id == 12:
            to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(role = roles.SUPERADMIN) | Q(id = instance.owner_user_obj_id))
        else:
            to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(role = roles.VERIFIER) | Q(role = roles.SUPERADMIN) | Q(id = instance.owner_user_obj_id))
        to_notification = to_notification.values_list('id', flat=True)

        from_notification =CustomUser.objects.filter(role = roles.ADMIN).first().id

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

    # Save the new notification object
    notification = serializer.save()
    # Create a custom response
    response_data = {
        "message": "sample form Notification created successfully ",
        "data": serializer.data,
    }

    return response_data, status.HTTP_201_CREATED



    