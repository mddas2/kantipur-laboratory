from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView
from rest_framework.routers import DefaultRouter
from .views import PermissionAllDelete

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView,TokenVerifyView

router = DefaultRouter()

router.register('users', views.CustomUserSerializerViewSet, basename="CustomUserSerializer")
router.register('groups', views.GroupViewSet, basename="group")
router.register('permissions', views.PermissionViewSet, basename="permission")

urlpatterns = [    
    path('auth/login/', LoginView.as_view()),
    path('', include(router.urls)),

    path('gettoken/',TokenObtainPairView.as_view(),name="token_obtain_pair"),
    path('refresh-token',TokenRefreshView.as_view(),name = 'refresg-token'),
    path('token-verify/',TokenVerifyView.as_view(),name="token_verify"),

    path('permission-all-delete/', PermissionAllDelete.as_view()),

    # path('user-has-groups/',)
    
]