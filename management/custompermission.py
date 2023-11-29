from rest_framework.permissions import BasePermission
from . import roles

def IsAuthenticated(request):
    return bool(request.user and request.user.is_authenticated)

def AdminLevelPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ADMIN, roles.SMU , roles.SUPERADMIN]

def AnalystPermission(request):
    return IsAuthenticated(request) and request.user.role in [roles.ANALYST]

class SampleFormViewSetPermission(BasePermission):
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
            #print("SDasd asd")
            return True
        elif method_name == 'destroy':
            return False
        else:
            return False

class CommodityViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class MicroparameterViewsetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AnalystPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AnalystPermission(request)
        elif method_name == 'partial_update':
            return AnalystPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class FiscalYearPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if request.user.role != roles.SUPERADMIN:
            return False

        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return True
        elif method_name == 'partial_update':
            return False
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class RejectSampleFormViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        return True
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
            return True
        else:
            return False
class CommodityCategoryViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class TestResultViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class PaymentViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return AdminLevelPermission(request)
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return AdminLevelPermission(request)
        elif method_name == 'partial_update':
            return AdminLevelPermission(request)
        elif method_name == 'destroy':
            return False
        else:
            return False
        
class SampleFormHasVerifierViewSetPermission(BasePermission):
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

class ClientCategoryPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return False
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return False
        elif method_name == 'partial_update':
            return False
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


    

