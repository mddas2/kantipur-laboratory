from django.urls import path,include
from .views import TrackSample


urlpatterns = [
    path('track-sample/<int:pk>/',TrackSample.as_view(),name='track-sample')
]