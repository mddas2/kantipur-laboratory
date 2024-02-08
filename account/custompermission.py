from rest_framework.permissions import BasePermission
from management import roles


def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def fullAdminPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SMU , roles.SUPERADMIN, roles.VERIFIER,roles.SUPERVISOR,roles.ANALYST]


class AccountPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        # print(method_name)
        if method_name == 'list':
            return True
        elif method_name == 'create':
            #check 
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            #check update role , if  role is user then only can updte there own account. for update all role must be ADMIN
            return True
        elif method_name == 'partial_update':
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False
    
class AdminLevelPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return fullAdminPermission(request)
        else:
            # Default to denying permission for unknown methods
            return False
      