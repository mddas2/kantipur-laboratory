from account.models import CustomUser
from .models import Notification
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting
from . import mapping_notification_type
from emailmanagement.email_sender import ESendMail

def NotificationHandler(instance, request,method,model_name):
    if method == "update":
        notification_message = str(instance.username) + " has been modified"
        particular_message = "Your aaccount has been modified"
        to_notification = [instance.id]
    if method == "create":
        notification_message=str(instance.username) + " is arrived"
        particular_message = "Welcome Here"
        to_notification = [instance.id]
    path = frontend_setting.user_request
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
        'isinstance_id':instance.id
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

    to_email = CustomUser.objects.values_list('email', flat=True)
    # ESendMail(notification_message,to_email)
    return response_data, status.HTTP_201_CREATED

def sampleFormNotificationHandler(instance,notification_type):

    notification_message = mapping_notification_type.mapping[notification_type]['admin_message']
    particular_message = mapping_notification_type.mapping[notification_type]['user_message']
    model_name = mapping_notification_type.mapping[notification_type]['model_name']
    path = mapping_notification_type.mapping[notification_type]['path']

    group_notification = mapping_notification_type.mapping[notification_type]['to_users']
    group_notification = ','.join(group_notification)


    from_notification = mapping_notification_type.mapping[notification_type]['from_user']
    from_notification = ','.join(from_notification)

    to_notification = CustomUser.objects.values_list('id', flat=True) #mapping_notification_type.mapping['new_sample_form']['from_user']

    is_read = False


   
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
        'isinstance_id':instance.id
    }

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



    