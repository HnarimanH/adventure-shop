from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.validators import UniqueValidator
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes



class UserRegisterSerializer(serializers.ModelSerializer):
    
        
    # validating the email and usenrame via UniqueValidator to check if the username or email exist.
    
    email = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Email already asigned to another account.")]
    )
    username = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all(), message="Username already taken.")]
    )
    
    
    

    class Meta:
        
        # Using Django's built-in User model for registration
        model = User
        
        
        # Limit serializer to only expose username and password fields
        fields = ['username', 'first_name', 'last_name', 'email','password']
        extra_kwargs = {'password': {'write_only': True}}
        
        

    def create(self, validated_data):
        
        # Creates and returns a new user with hashed password
        user =  User.objects.create_user(
            
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            
        )
        user.is_active = False
        user.save()
        return user
        
        
        
class UserLoginSerializer(serializers.Serializer):
    
    # Define expected fields for login input (email & password)
    email = serializers.CharField()
    password = serializers.CharField(write_only = True)
    
    
    
    
    
    
    
    
    def validate(self, data):
        

        
    
        
        try:
            userObj = User.objects.get(email=data.get('email')).username
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid username or password")
        # Authenticates user with provided credentials against the database
        user = authenticate(
            username= userObj,
            password= data.get('password')
        )
        
        
       # If authentication fails, raise a validation error
        # If successful, attach user object to validated data   
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        if not user.is_active:
            return serializers.ValidationError("Please verify your email before logging in.")
    
        data['user'] = user
        return data
    
        


class UserForgotPasswprdSerializer(serializers.Serializer):
    email = serializers.CharField()
    
    def validate(self, data):
        try:
            user = User.objects.get(email=data.get('email'))
        except User.DoesNotExist:
            raise serializers.ValidationError("Email not registered")
            
        token = PasswordResetTokenGenerator().make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        
        data['uid'] = uid
        data['token'] = token
        data['user'] = user  

        return data
    
    
    