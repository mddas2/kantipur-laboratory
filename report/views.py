import os
from django.conf import settings
from django.http import HttpResponse
from rest_framework import views

from django.shortcuts import render

class ReportDownload(views.APIView):
    def get(self, request):
        return render(request, 'report.html')
       