from rest_framework import serializers
from ..models import Branches,InspectorType

class InspectorTypeWriteSerializers(serializers.ModelSerializer):
    class Meta:
        model = InspectorType
        fields = '__all__'

class InspectorTypReadSerializers(serializers.ModelSerializer):
    class Meta:
        model = InspectorType
        fields = '__all__'
