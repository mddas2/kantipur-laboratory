from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models import Branches
from ..serializers.branch_serializers import BrancheReadSerializers,BrancheWriteSerializers

class BranchesViewSets(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]
    queryset = Branches.objects.all()

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BrancheWriteSerializers
        elif self.action in ['list']:
            return  BrancheReadSerializers
        return super().get_serializer_class()
    