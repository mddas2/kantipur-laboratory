from rest_framework.permissions import BasePermission
from management import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def SmuSuperAdmin(request):
    return bool(IsAuthenticated(request) and request.user.role in [roles.SMU,roles.SUPERADMIN])

class AdmnLevelPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return SmuSuperAdmin(request)
        else:
            False
            