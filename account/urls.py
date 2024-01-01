from account.views import UserRegistrationView,UserLoginView,UserProfileView,ChangePasswordView,SendPasswordResetEmailView,ResetPasswordView
from django.urls import path,include

urlpatterns = [
     path('register/', UserRegistrationView.as_view(), name='register'),
     path('login/', UserLoginView.as_view(), name='login'),
     path('profile/', UserProfileView.as_view(), name='profile'),
     path('sent-reset-password-email/', SendPasswordResetEmailView().as_view(), name='sent-reset-password-email'),
     path('changepassword/', ChangePasswordView.as_view(), name='change-password'),
     path('reset-password/<uid>/<token>/',ResetPasswordView().as_view(), name='reset-password'),

]