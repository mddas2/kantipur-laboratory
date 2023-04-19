from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import LoginView,PermissionAllDelete


router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")
router.register('users', views.CustomUserSerializerViewSet, basename="CustomUserSerializer")
router.register('group', views.GroupViewSet, basename="group")
router.register('permission', views.PermissionViewSet, basename="permission")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.Home,name='Home'),
    path('auth/login/', LoginView.as_view()),
    # path('auth/',include('rest_framework.urls',namespace="login"),name='login_name'),
    path('permission-all-delete/', PermissionAllDelete.as_view()),
]