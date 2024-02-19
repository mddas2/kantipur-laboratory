from rest_framework.routers import DefaultRouter
from .viewsets import branch_viewset
from django.urls import  path,include

router = DefaultRouter()
router.register('', branch_viewset.BranchesViewSets, basename="branch_viewset")

urlpatterns = [
    path('', include(router.urls)),
]