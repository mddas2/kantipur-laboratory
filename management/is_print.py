from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import SampleForm
from rest_framework import status
from rest_framework.response import Response
from . import roles

class SampleFormIsPrint(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self,request,sample_form,format = None):
        if request.user.role == roles.SMU:
            is_print = request.data.get('is_print')
            sample_form_obj = SampleForm.objects.get(id = sample_form)
            sample_form_obj.is_print = is_print
            sample_form_obj.save()
            response_data = {
                "message": "update successfully",
                "is_print": is_print,
                "sample_form_id": sample_form
            }

            # Return the custom response
            return Response(response_data, status=status.HTTP_201_CREATED)
        
        response_data = {
                "message": "you are not smu",
                "is_print": is_print,
                "sample_form_id": sample_form
        }
        # Return the custom response
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        

    