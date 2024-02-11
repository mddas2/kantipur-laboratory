from rest_framework import views
from rest_framework.response import Response

class GetStatus(views.APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
        
    def get(self, request, format=None,url=None):
        import json
        status = [
            {
                'name': 'Pending',
                'value': 'pending', 
            },
            {
                'name': 'Processing',
                'value': 'processing', 
            },
            {
                'name': 'Not Assigned',
                'value': 'not_assigned',
            },
            {
                'name': 'Not Verified',
                'value': 'not_verified',
            },
            {
                'name': 'Completed',
                'value': 'completed',
            },
            {
                'name': 'Recheck',
                'value': 'recheck',
            },
            {
                'name': 'Rejected',
                'value': 'rejected',
            }
        ]

        return Response(status)