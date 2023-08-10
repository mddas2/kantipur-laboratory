from django.shortcuts import render
from rest_framework import generics, status, viewsets, response
from .serializers import EmailSerializer, CustomPasswordResetSerializer,CustomEmailVerifySerializer
from account.models import CustomUser
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

site_f  = "https://dev-lims.netlify.app"#"https://lims.dftqc.gov.np"

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
            reset_url = f"Click the link to reset your password: {site_f}/password-reset?pk={encoded_pk}&token={token}"
            email = user.email
            subject = 'Password Reset Link'
            sendMail(email, reset_url,subject)
            
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

class EmailVerificationConfirmView(APIView):
    serializer_class = CustomEmailVerifySerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={"kwargs":kwargs})
        serializer.is_valid(raise_exception=True)
        
        return response.Response(
            {"message": "Email Verified Complete"},
            status=status.HTTP_200_OK,
        )

class SendEmailVerificationLink(APIView):
    
    def post(self, request, *args, **kwargs):
        import uuid
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({
                'detail': 'User with this email does not exist.',
            }, status=status.HTTP_400_BAD_REQUEST)

        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))
        token = PasswordResetTokenGenerator().make_token(user)

        # Generate a unique verification token
        verification_token = str(uuid.uuid4())

        # Send the token via email
        subject = 'Email Verification Token'
        message = f'Your email verification token is: {verification_token}'
        verify_url = f"{site_f}/email-verification?pk={encoded_pk}&token={token}"
        subject = 'Email Verification Link '
        sendMail(email,verify_url,subject)

        return Response({
            'detail': 'Email verificatio'})

def sendMail(email, reset_url,subject):
    message = reset_url
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    