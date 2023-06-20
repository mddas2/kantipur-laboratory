from account.models import CustomUser
from .models import Notification
from .serializer import NotificationWriteSerializer
from rest_framework import status
from . import frontend_setting

def userNotification(instance, request):
    print("handling notification")
    print(instance,request.user)
    notification_message = "A client Category has been created"
    path = frontend_setting.user_request
    try:
        from_notification = request.user.id
    except:
        from_notification = instance.id
    model_name = "CustomUser"
    is_read = False
    group_notification = "admin"

    # Get all users for notification recipients
    to_notification = CustomUser.objects.values_list('id', flat=True)
    print(to_notification)


    # Create notification data
    notification_data = {
        "notification_message": notification_message,
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

    return response_data, status.HTTP_201_CREATED


    