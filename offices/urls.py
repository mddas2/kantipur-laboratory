from rest_framework.routers import DefaultRouter
from .viewsets import branch_viewset,inspector_viewset
from django.urls import  path,include

router = DefaultRouter()
router.register('branch', branch_viewset.BranchesViewSets, basename="branch_viewset")
#router.register('inspector-type', inspector_viewset.InspectorViewSets, basename="branch_viewset")

urlpatterns = [
    path('', include(router.urls)),
]