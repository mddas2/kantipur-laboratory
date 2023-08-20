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

site_f  = "https://lims.dftqc.gov.np" #http://localhost:4200"#"https://dev-lims.netlify.app"#"https://lims.dftqc.gov.np"

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
            
            reset_url = f"{site_f}/password-reset?pk={encoded_pk}&token={token}"
            email = user.email
            subject = 'Password Reset Link'
            reset_verification = "reset_password"
            sendMail(email, reset_url,subject,reset_verification)
            
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
            {"message": "Email Verified Complete",'verified':True},
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

        # Send the token via email
        subject = 'Email Verification Token'
        verify_url = f"{site_f}/user-verification-success?pk={encoded_pk}&token={token}"
        subject = 'Email Verification Link '
        reset_verification = "verification"
        sendMail(email,verify_url,subject,reset_verification)

        return Response({
            'detail': 'Email verificatio'})

def sendMail(email, reset_url,subject,reset_verification):
    if reset_verification == "verification":
        body = f"""<div class="sent-message">
                <div class="sent-message-box">
                    <img src="../image/sent.gif" alt="">
                    <div class="success-message">
                        <h4>Please verify your email</h4>
                        <p>Check your email and click the link to activate your account.</p>
                        <h6 class="mt-5 mb-3">Didn't receive an email ?</h6>
                        <p><a class="badge" href="{reset_url}"  style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">Verify Email</a></p>
                    </div>
                </div>
            </div></html>"""
    else:
        body = f"""<body><div class="sent-message">
                <div class="sent-message-box">
                    <img src="../image/sent.gif" alt="">
                    <div class="success-message">
                        <h4>Please change your Password</h4>
                        <p>Check your email and click the link to change your account.</p>
                        <h6 class="mt-5 mb-3">click here ?</h6>
                        <p><a class="badge" href="{reset_url}"  style="text-decoration: none; background: #0B53A7; color: #FFFFFF; padding: 10px 20px; border-radius: 3px; display: inline-block; margin-top: 15px;">Change your Password</a></p>
                    </div>
                </div>
            </div></body></html>"""
    html_contents = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=\, initial-scale=1.0">
            <title>Verification Mail</title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha3/dist/css/bootstrap.min.css" rel="stylesheet"
                integrity="sha384-KK94CHFLLe+nY2dmCWGMq91rCGa5gtU4mk92HdvYe+M/SXH301p5ILy+dN9+nJOZ" crossorigin="anonymous">
            <style>
                @import url(https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap);

                .sent-message {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    font-family: Poppins;
                    height: 100vh;
                }

                .sent-message-box {
                    background: #ffffff;
                    padding: 40px;
                    border-radius: 8px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    border: 1px solid whitesmoke;
                }

                .success-message {
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                }

                .success-message h4 {
                    color: #2460b9;
                    font-weight: 600;
                }

                .sent-message-box img {
                    height: 100px;
                    width: 100px;
                    margin-bottom: 20px;
                }

                .badge {
                    background: #2460b9;
                    font-family: Poppins;
                    font-weight: 500;
                    font-size: 13px;
                    color: #141414;
                    padding: 14px 20px;
                    text-decoration: none;
                    color: #ffffff;
                    border-radius: 3px;
                }

                .badge:hover {
                    background: #0d6efd;
                    color: #ffffff;
                }
            </style>
        </head>""" + body
    
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    plain_message = ""
    send_mail(subject, plain_message, email_from, recipient_list,html_message=html_contents)
    