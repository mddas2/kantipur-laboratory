from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
<<<<<<< HEAD
=======
from .views import LoginView,PermissionAllDelete

>>>>>>> 6aaeb406badf642582cfad26e6b6061cb8607339

router = DefaultRouter()
router.register('client-category', views.ClientCategoryViewSet, basename="api/client_category")
router.register('sample-form', views.SampleFormViewSet, basename="sample_form")
router.register('commodity', views.CommodityViewSet, basename="commodity")
router.register('commodity-category', views.CommodityCategoryViewSet, basename="commodity_category")
router.register('users', views.CustomUserSerializerViewSet, basename="CustomUserSerializer")
router.register('group', views.GroupViewSet, basename="group")
router.register('permission', views.PermissionViewSet, basename="permission")

urlpatterns = [
<<<<<<< HEAD
    path('', include(router.urls)),
    # path('', views.Home,name='Home'),
=======
    path('api/', include(router.urls)),
    path('', views.Home,name='Home'),
    path('auth/login/', LoginView.as_view()),
>>>>>>> 6aaeb406badf642582cfad26e6b6061cb8607339
    # path('auth/',include('rest_framework.urls',namespace="login"),name='login_name'),
    path('permission-all-delete/', PermissionAllDelete.as_view()),
]