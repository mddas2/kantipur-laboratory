from .models import Notification
from rest_framework import serializers


class NotificationReadSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = Notification
        fields = '__all__'
    
class NotificationWriteSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Notification
        fields = '__all__'


 