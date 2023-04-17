from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('client_category', views.ClientCategoryViewSet, basename="client_category")
router.register('sample_form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('commodity_category', views.CommodityCategoryViewSet, basename="commodity_category")

urlpatterns = [
    path('', include(router.urls)),
    path('auth/',include('rest_framework.urls',namespace="login")),
]