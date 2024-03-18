from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TrackSample,BackSampleFormViewset
from .import back_to

router = DefaultRouter()

router.register('back-sample-form',BackSampleFormViewset,basename='backsampleviewset')


urlpatterns = [
    path('',include(router.urls)),
    path('track-sample/<int:pk>/',TrackSample.as_view(),name='track-sample'),
    path('back-to/<int:role>/<str:sample_form>/',back_to.Backto.as_view(),name='track-sample')
]