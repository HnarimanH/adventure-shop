from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserForgotPasswprdSerializer
from rest_framework import status
from django.contrib.auth import login
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
import os
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


logger = logging.getLogger(__name__)
def cleanup_unverified_users():
        cutoff_time = timezone.now() - timedelta(minutes=2)
        users_to_delete = User.objects.filter(is_active=False, date_joined__lt=cutoff_time)
        print(users_to_delete.count())
        users_to_delete.delete()

        


    

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(APIView):
    def post(self, request):
        cleanup_unverified_users() 
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"https://localhost:5173/?uid={uid}&token={token}"

            send_mail(
                subject='Adventure shop Email verification',
                message=f'please verify you email at Adventure shop by clicking the link: {verification_link}.',
                from_email='noreply@gmail.com',
                recipient_list=[request.data.get('email')],
                fail_silently=False
            )
            return Response({"message": "Verification Email sent!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
    
   
@method_decorator(csrf_exempt, name='dispatch') 
class EmailVerificationView(APIView): 
    def post(self, request):
        # gets data from request 
        token = request.data.get("token")
        uid = request.data.get("uid")
        
        if not token or not uid:
            return Response({"errors":"Token and Uid are required" }, status=400)
        
        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"errors":"Invalid uid" }, status=400)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"errors":"Invalid or expired token" }, status=400)
        
        user.is_active = True
        user.save()
        return Response({"message": "Email verified successfully!"})
    
    
    
    
    
    
    
    
    
    

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)
            refreshToken = RefreshToken.for_user(user)
            return Response({
                "access":str(refreshToken.access_token),
                "refresh":str(refreshToken),
                "is_superuser": user.is_superuser
            })
        return Response({"message": "invalid request"})













@method_decorator(csrf_exempt, name='dispatch')
class ForgotPassView(APIView):
    def post(self, request):
        serializer = UserForgotPasswprdSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            email = data['user'].email
            newpassword = data['password']
            token = data['token']
            uid = data['uid']

            # Build a reset link (frontend route)
            reset_link = f"https://localhost:5173/?uid={uid}&token={token}&email={email}&newpassword={newpassword}"

            send_mail(
                subject='Adventure Shop Password Reset',
                message=f'Click the link to reset your password: {reset_link}',
                from_email='noreply@gmail.com',
                recipient_list=[email],
                fail_silently=False
            )

            return Response({"message": "Password reset email sent."})
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@method_decorator(csrf_exempt, name='dispatch') 
class ResetPasswordView(APIView):
    def post(self, request):
        uid = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid UID"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password successfully reset."})