from rest_framework.permissions import BasePermission

class ClientCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return True
        elif method_name == 'partial_update':
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class SampleFormHasParameterPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return True
        elif method_name == 'partial_update':
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False


    

