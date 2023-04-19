from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView
from rest_framework.routers import DefaultRouter
from .views import PermissionAllDelete

router = DefaultRouter()

router.register('users', views.CustomUserSerializerViewSet, basename="CustomUserSerializer")
router.register('groups', views.GroupViewSet, basename="group")
router.register('permissions', views.PermissionViewSet, basename="permission")

urlpatterns = [    
    path('auth/login/', LoginView.as_view()),
    path('', include(router.urls)),
    path('permission-all-delete/', PermissionAllDelete.as_view()),
    
]