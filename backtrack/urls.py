from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import TrackSample
from .import back_to


urlpatterns = [
    path('track-sample/<int:pk>/',TrackSample.as_view(),name='track-sample'),
    path('back-to/<int:role>/<str:sample_form>/',back_to.Backto.as_view(),name='track-sample')
]