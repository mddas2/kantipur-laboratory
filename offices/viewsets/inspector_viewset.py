from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Branches
from ..serializers.inspector_serializers import InspectorTypReadSerializers,InspectorTypeWriteSerializers
from ..utilities.pagination import MyPageNumberPagination

class InspectorViewSets(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    queryset = Branches.objects.all()
    pagination_class = MyPageNumberPagination
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return InspectorTypeWriteSerializers
        elif self.action in ['list']:
            return  InspectorTypReadSerializers
        return super().get_serializer_class()
    