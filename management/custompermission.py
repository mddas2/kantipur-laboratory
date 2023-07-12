from rest_framework.permissions import BasePermission

class SampleFormViewSetPermission(BasePermission):
    def has_permission(self, request, view):
        method_name = view.action
        print(method_name)
        if method_name == 'list':
            return True
        elif method_name == 'create':
            return True
        elif method_name == 'retrieve':
            return True
        elif method_name == 'update':
            return True
        elif method_name == 'partial_update':
            print("SDasd asd")
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
        
class TestResultViewSetPermission(BasePermission):
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
        
class PaymentViewSetPermission(BasePermission):
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


    

