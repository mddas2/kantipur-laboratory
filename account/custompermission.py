from rest_framework.permissions import BasePermission

class Account(BasePermission):
    def has_permission(self, request, view):
        #condition 
        print("i am permission asjdlkajsalakdjjalks ds")
        return False
        return False #if condition false
    

