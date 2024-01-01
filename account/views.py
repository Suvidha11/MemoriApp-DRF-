from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from account.renderers import UserRenderers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from account.serializers import*
# from account.utils import Util



# generate token manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    
    def post(self,request,formet=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            token=get_tokens_for_user(user)
            
            return Response({"token":token,"msg":"registration success"},status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserLoginView(APIView):
    renderer_classes = [UserRenderers]
    def post(self,request,formet=None):
        serializer=UserLoginSerializer(data=request.data)
        
        if serializer.is_valid(raise_exception=True):
            email=serializer.data.get("email")
            password=serializer.data.get("password")
            user=authenticate(email=email, password=password)
            if user is not None: 
                token = get_tokens_for_user(user)
                
                return Response({"token":token,"msg":"login success"},status=status.HTTP_200_OK)
            else: 
                return Response({"errors":{"non_field_errors":["Email and Password is not valid"]}}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes= [IsAuthenticated]
    def get(self,request,formet=None):
        serializer=UserProfileSerializer(request.user) 
        return Response(serializer.data,status=status.HTTP_200_OK)
    

class ChangePasswordView(APIView):
    renderer_classes = [UserRenderers]
    permission_classes= [IsAuthenticated]
    def post(self,request,formet=None):
        serializer=ChangePasswordSerializer(data=request.data,context={'user':request.user})
       
        if serializer.is_valid(raise_exception=True):
             return Response({"msg":"Password Change Successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class SendPasswordResetEmailView(APIView):
    renderer_classes = [UserRenderers]
    def post(self,request,formet=None):
        serializer=SendPasswordResetEmailSerializer(data=request.data,context={'user':request.user})     
        if serializer.is_valid(raise_exception=True):
            # email=serializer.data.get("email")
            return Response({"msg":"Password Reset link Send. Please check your  link"},status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Reset pasword view
class ResetPasswordView(APIView):
    renderer_classes = [UserRenderers]   
    def post(self, request, uid, token, formet=None):
        serializer=ResetPasswordSerializer(data=request.data,context={'uid':uid, 'token':token})     
        if serializer.is_valid(raise_exception=True):
            return Response({"msg":"Password Reset successfully"},status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
