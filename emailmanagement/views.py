from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from .serializers import EmailSerializer, CustomPasswordResetSerializer
from account.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


class EmailCheckView(generics.GenericAPIView):
    serializer_class = EmailSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data["email"]
        user = CustomUser.objects.filter(email=email).first()
        if user:
            encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
            token = PasswordResetTokenGenerator().make_token(user)
            
            # reset_url = reverse(
            #     "reset-password",
            #     kwargs={"encoded_pk":encoded_pk, "token":token}
            # )
            reset_url = f"https://lims-home.netify.app/password-reset?pk={encoded_pk}&token={token}"
            email = user.email
            
            sendMail(email, reset_url)
            
            return response.Response(
                {
                "message": "password reset link has been sent to your email address"
                },
                status=status.HTTP_200_OK,
            )
        else:
            return response.Response(
                {"message": "User doesn't exists"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CustomPasswordResetView(generics.GenericAPIView):
    serializer_class = CustomPasswordResetSerializer
    
    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            {"message": "Password Reset Complete"},
            status=status.HTTP_200_OK,
        )


def sendMail(email, reset_url):
    subject = 'Password Reset Link'
    message = f'Click the link to reset your password: {reset_url}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    