from rest_framework import serializers
from management.models import ClientCategoryDetail,ClientCategoryDetailImages


class ClientCategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategoryDetail
        fields = '__all__'
    
class ClientCategoryDetailImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientCategoryDetailImages
        fields = '__all__'
    