from .models import Notification
from rest_framework import serializers

class NotificationReadSerializer(serializers.ModelSerializer):        
    class Meta:
        model = Notification
        fields = '__all__'
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_role = self.context['request'].user.role
        # path = representation.get('path',None)
        print(user_role," user role ")
        return representation
    
class NotificationWriteSerializer(serializers.ModelSerializer): 

    class Meta:
        model = Notification
        fields = '__all__'


 