from django.urls import path
from .views import EmailCheckView, CustomPasswordResetView


urlpatterns = [
    path('password-reset/', EmailCheckView.as_view()),
    path('password-reset/<str:encoded_pk>/<str:token>/', CustomPasswordResetView.as_view(), name="reset-password"),
]
