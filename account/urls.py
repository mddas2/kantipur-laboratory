from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView


urlpatterns = [    
    path('auth/login/', LoginView.as_view())
]