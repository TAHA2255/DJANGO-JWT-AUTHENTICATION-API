from django.shortcuts import render
from .serializers import UserRegisterSerializer,UserLoginSerializer,UserProfileSerializer,ChangePassSerializer,PassResetEmailSerializer,PassResetSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.contrib.auth.hashers import check_password
# Create your views here.

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegisterView(APIView):
    def post(self,request,format=None):
        user = UserRegisterSerializer(data=request.data)
        if user.is_valid():
            valid_user = user.save()
            token = get_tokens_for_user(valid_user)
            return Response({'token':token,'msg':'registration successfull'},status=status.HTTP_201_CREATED)
        return Response({'msg':'registration unsuccessful'},status=status.HTTP_400_BAD_REQUEST)
        

class UserLoginView(APIView):
    def post(self,request,format=None):
        user = UserLoginSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        email = request.data.get('email')
        password = request.data.get('password')
        auth = authenticate(email=email, password=password)
        if auth is not None:
            token = get_tokens_for_user(auth)
            return Response({'token': token,'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request,format=None):
        user = UserProfileSerializer(request.user)
        return Response(user.data)

class ChangePassView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        serializer= ChangePassSerializer(data=request.data,context={'user':request.user})
        serializer.is_valid(raise_exception=True)
        return Response({'msg':'password changed successfully'},status=status.HTTP_200_OK)

class PasswordResetEmailView(APIView):
    def post(self,request):
        serializer = PassResetEmailSerializer(data=request.data)
        if serializer.is_valid():
           return Response({'msg':'password reset link has been sent to your email'},status=status.HTTP_200_OK)
        return Response({'msg':'Enter the correct email'},status=status.HTTP_200_OK)

class PasswordRestView(APIView):
    def post(self,request,uid,token,format=None):
        serialize = PassResetSerializer(data=request.data,context={'uid':uid,'token':token})
        if serialize.is_valid():
            return Response({'msg':'your password has been reset'},status=status.HTTP_200_OK)
        return Response({'msg':'Invalid request'},status=status.HTTP_400_BAD_REQUEST)


