from . import views,preeti_to_unicode
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [   
    path('get-report', views.ReportDownload.as_view()),
    path('preeti-to-unicode', preeti_to_unicode.PreetiToUniCode.as_view()),
    path('unicode-to-preeti', preeti_to_unicode.UnicodeToPreeti.as_view()),
]