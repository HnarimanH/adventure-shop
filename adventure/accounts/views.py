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






from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)
def cleanup_unverified_users(self, *args, **kwargs):
        cutoff_time = timezone.now() - timedelta(minutes=2)
        users_to_delete = User.objects.filter(is_active=False, date_joined__lt=cutoff_time)
        users_to_delete.delete()

        


    
    
class RegisterView(APIView):
    def post(self, request):
        cleanup_unverified_users() 
        serializer = UserRegisterSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            verification_link = f"http://localhost:5173/?uid={uid}&token={token}"
            print("EMAIL BEING USED:", request.data.get('email'))
            send_mail(
                subject='Adventure shop Email verification',
                message=f'please verify you email at Adventure shop by clicking the link: {verification_link}.',
                from_email='noreply@gmail.com',
                recipient_list=[request.data.get('email')],
                fail_silently=False
            )
            return Response({"message": "Verification Email sent!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
    
    
    
    
    
    
    
class EmailVerificationView(APIView): 
    def post(self, request):
    
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
    
    
    
    
    
    
    
    
    
    
    
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)
            refreshToken = RefreshToken.for_user(user)
            return Response({
                "access":str(refreshToken.access_token),
                "refresh":str(refreshToken)
            })
        return Response({"message": "invalid request"})













class ForgotPassView(APIView):
    def post(self, request):
        serializer = UserForgotPasswprdSerializer(data = request.data)
        if serializer.is_valid():
            send_mail(
                subject='Test Email',
                message='Bananas are yellow. This is a test.',
                from_email='noreply@gmail.com',
                recipient_list=[request.data.get('email')],
                fail_silently=False
            )
            return Response({"message": "Email sent!"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)