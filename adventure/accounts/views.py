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
from .models import MyUser
import os
from pathlib import Path
from dotenv import load_dotenv
from django.utils import timezone
from datetime import timedelta
import logging
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt




BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / '.env', override=True) 


logger = logging.getLogger(__name__)
def cleanup_unverified_users():
        cutoff_time = timezone.now() - timedelta(minutes=2)
        users_to_delete = MyUser.objects.filter(is_active=False, date_joined__lt=cutoff_time)
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
            verification_link =f"{os.getenv('CORS_ORIGINS', '').split(',')[0]}/?uid={uid}&token={token}"
            print(verification_link)
            send_mail(
                subject='Adventure shop Email verification',
                message=f"""Hey there, brave adventurer.

                Thanks for signing up at Adventure Shop. But before you storm the gates of glory, we need you to verify your email.

                Click the magical link below to activate your account:

                🔗 [{verification_link}]

                If you didn’t sign up, just ignore this message. Or forward it to someone who deserves a good time.

                See you on the other side,
                The Adventure Shop Goblins 🛒⚔️

                P.S. This link expires faster than a discount on swords.""",
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
            user = MyUser.objects.get(pk=uid)
        except Exception:
            return Response({"errors":"Invalid uid" }, status=400)
        
        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"errors":"Invalid or expired token" }, status=400)
        
        user.is_active = True
        user.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_superuser": user.is_superuser,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "profilePic": user.profilePic
        })
    
    
    
    


@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data = request.data)
        if serializer.is_valid(): 
            user = serializer.validated_data['user']
            login(request, user)
            refresh = RefreshToken.for_user(user)
            print(user.profilePic)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "is_superuser": user.is_superuser,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "username": user.username,
                "profilePic": user.profilePic
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

            # reset link (frontend route)
            reset_link = f"{os.getenv('CORS_ORIGINS', '').split(',')[0]}/?uid={uid}&token={token}&newpassword={newpassword}"

            send_mail(
                subject='Adventure Shop Password Reset',
                message=f"""Hey adventurer,

                Looks like you forgot your password. No big deal. Happens to everyone even the best sword slingers.

                Click the link below to reset it and get back to conquering:

                🔗 [{reset_link}]

                This link is only valid for a short time, so don’t take too long. The dungeon won’t clear itself.

                If you didn’t request this reset, ignore this email. No spells were cast.

                Stay strong,  
                – The Adventure Shop Team 🛡️""",
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
            user = MyUser.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Invalid UID"}, status=400)

        if not PasswordResetTokenGenerator().check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password successfully reset."})