from django.urls import path
from .views import RegisterView, LoginView, ForgotPassView, EmailVerificationView, ResetPasswordView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('forgotPass/', ForgotPassView.as_view(), name='forgotPass'),
    path('emailverification/', EmailVerificationView.as_view(), name='emailverification'),
    path('resetpassword/', ResetPasswordView.as_view(), name='resetpassword'),
]
