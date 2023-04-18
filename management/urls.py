from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.Home,name='Home'),
    path('auth/',include('rest_framework.urls',namespace="login")),
]