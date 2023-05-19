from . import views,preeti_to_unicode,preeti_to_pdf
from django.urls import path, include
from rest_framework.routers import DefaultRouter

urlpatterns = [   
    path('get-report/<str:report_name>/<str:report_type>/<str:report_lang>/', views.ReportDownload.as_view()),
    path('preeti-to-unicode', preeti_to_unicode.PreetiToUniCode.as_view()),
    path('unicode-to-preeti', preeti_to_unicode.UnicodeToPreeti.as_view()),
    path('preeti-to-pdf', preeti_to_pdf.PreetiToPdf,name="Preeti-to-pdf"),
]