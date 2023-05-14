from . import views
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [   
    path('get-report', views.ReportDownload.as_view()),
]