from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import views as auth_views , get_user_model
from django.urls import reverse_lazy
from main.serializers import UserSerializer , LoginSerializer
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from main.models import  User
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
# Create your views here.
# Create your views here.
class SignupView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            user_data = UserSerializer(user).data
            user_data['token'] = token.key
            return Response(user_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            user.logged_in = True
            user.save()
            
            token, created = Token.objects.get_or_create(user=user)
            
            user_data = UserSerializer(user).data
            user_data['token'] = token.key
            
            return Response(user_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


User = get_user_model()
class LogoutView(APIView):
    def post(self, request):
        # Get the token from the 'Authorization' header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return Response({"error": "Authorization header is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Token is in the format: 'Token <token>'
        parts = auth_header.split()

        # Ensure the header is properly formatted
        if len(parts) != 2 or parts[0].lower() != 'token':
            return Response({"error": "Invalid token format. Expected 'Token <token>'."}, status=status.HTTP_400_BAD_REQUEST)

        token = parts[1]  # Extract the token

        # Assuming each user has a unique token saved in a field like 'auth_token'
        try:
            user = User.objects.get(auth_token=token)
        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user is logged in
        if not getattr(user, "logged_in", True):
            return Response({"error": "User is already logged out."}, status=status.HTTP_400_BAD_REQUEST)

        # Mark the user as logged out
        user.logged_in = False
        user.save()
        
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    

authentication_classes = [TokenAuthentication]        