from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import PermissionAllDelete


router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="api/client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")
router.register('users', views.CustomUserSerializerViewSet, basename="CustomUserSerializer")
router.register('group', views.GroupViewSet, basename="group")
router.register('permission', views.PermissionViewSet, basename="permission")

urlpatterns = [
    path('', include(router.urls)),
    path('permission-all-delete/', PermissionAllDelete.as_view()),
]