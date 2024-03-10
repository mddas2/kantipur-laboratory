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
    return True
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
    is_read = False
    group_notification = "admin"
    

    # Create notification data
    notification_data = {
        "notification_message": notification_message,
        'particular_message':particular_message,
        "path": path,
        "from_notification": from_notification,
        "model_name": model_name,
        "is_read": is_read,
        "group_notification": 'USER_ADMIN',
        "to_notification": to_notification,
        'instance_id':instance.id,
        'notification_type':notification_type
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
    print(notification_type)
    if notification_type == "new_sample_form":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message =  notification_message.format(sample_id = instance.id,username = instance.owner_user_obj_id)
        refrence_number = encode_decode.generateEncodeIdforSampleForm(instance.id, "user")
        particular_message =  particular_message.format(refrence_number = refrence_number)

        to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(id = instance.owner_user_obj_id))
        to_notification = to_notification.values_list('id', flat=True)

        from_notification = instance.owner_user_obj_id
   
    elif notification_type == "assigned_supervisor":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_lab_id = instance.sample_form.sample_lab_id)
        to_notification = [instance.supervisor_user_id]  # here instance is supervisoruser

        from_notification = CustomUser.objects.filter(role = roles.SMU).first()

    elif notification_type == "assigned_analyst":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.id)

        notification_message = notification_message.format(sample_lab_id = instance.sample_form.sample_lab_id)

        to_notification = [instance.analyst_user_id] # here instance is sampleformhasparameter
        from_notification = instance.supervisor_sample_form.supervisor_user_id

    elif notification_type == "assigned_verifier":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path']+str(instance.sample_form.sample_lab_id)

        notification_message = notification_message.format(sample_lab_id = instance.sample_form.sample_lab_id)

        to_notification = CustomUser.objects.filter(role = roles.VERIFIER)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification = instance.sample_form.supervisor_sample_form.first().supervisor_user_id

    elif notification_type == "assigned_admin":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path'] + str(instance.sample_form.id)

        notification_message = notification_message.format(sample_lab_id = instance.sample_form.sample_lab_id)

        to_notification = CustomUser.objects.filter(role = roles.ADMIN)
        to_notification = to_notification.values_list('id', flat=True)
        from_notification =CustomUser.objects.filter(role = roles.VERIFIER).first().id

    elif notification_type == "approved_sample_form":
        notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
        particular_message = mapping_notification_type.mapping[notification_type]['user_message']
        path = mapping_notification_type.mapping[notification_type]['path']

        notification_message = notification_message.format(sample_lab_id = instance.sample_lab_id)

        to_notification = CustomUser.objects.filter(Q(role = roles.SMU) | Q(role = roles.ADMIN) | Q(id = instance.owner_user_obj_id))
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
    print(notification_data)
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



    