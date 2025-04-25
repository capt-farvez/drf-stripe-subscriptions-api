from django.shortcuts import render
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny

# Register new user
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allows public access
    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([name, email, password]):  # Check if all fields are provided
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST) 
        
        if User.objects.filter(email=email).exists():  # Check if email already exists
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(   # Create user with the custom manager
            email=email,
            password=password
        )
        user.name = name
        user.save() 

        return Response({"message": "User registered successfully."})
        
    
# Login and generate JWT tokens
class LoginView(APIView):
    permission_classes = [AllowAny]  # Allows public access
    
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)  # Generate refresh token
                return Response({
                    "refresh_token": str(refresh),
                    "access_token": str(refresh.access_token),  # Generate access token
                    "user": {
                        "id": str(user.id),
                        "name": user.name,
                        "email": user.email,
                    }
                })
            else:
                return Response({"error": "Invalid credentials."}, status=400)
        except User.DoesNotExist:
            return Response({"error": "User does not exist."}, status=404)
        

# Logout and blacklist refresh token
class LogoutView(APIView):
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token')  # Get refresh token from request
            token = RefreshToken(refresh_token)  # Create token object
            token.blacklist() # Blacklist the token to prevent further use
            return Response({"message": "Logged out successfully."})
        except Exception as e:
            return Response({"error": str(e)}, status=400)
        

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:  # Check if user is authenticated
            # Fetch user profile data
            profile_data = {
                "name": user.name,
                "email": user.email,
                "is_subscribed": user.is_subscribed,
                "subscription_start_date": user.subscription_start_date,
                "subscription_end_date": user.subscription_end_date,
            }
            return Response(profile_data)
        else:
            return Response({"error": "User not authenticated."}, status=401)

    def put(self, request):
        user = request.user
        if user.is_authenticated:  # Check if user is authenticated
            name = request.data.get('name')
            email = request.data.get('email')

            if name:
                user.name = name
            if email:
                user.email = email

            user.save()
            return Response({"message": "Profile updated successfully."})
        else:
            return Response({"error": "User not authenticated."}, status=401)

    def delete(self, request):
        user = request.user
        if user.is_authenticated:
            user.delete()
            return Response({"message": "User account deleted successfully."})
        else:
            return Response({"error": "User not authenticated."}, status=401)
