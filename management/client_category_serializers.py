from rest_framework import serializers
from management.models import ClientCategoryDetail


class ClientCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategoryDetail
        fields = '__all__'
