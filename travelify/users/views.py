from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer, UserSerializer

# Register User (Signup)
@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    try:
        data = request.data
        username = data.get('email')  # Using email as username
        password = data.get('password')
        email = data.get('email')
        role = data.get('role', 'general_user')  # Default role is 'general_user'
        name = data.get('name', '')

        if CustomUser.objects.filter(username=username).exists():
            return Response({"ofBackendMessage": "This email is already registered. Try logging in."}, status=400)

        # Create User
        user = CustomUser.objects.create_user(
            username=username, password=password, email=email, role=role, name=name
        )
        user.save()

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "ofBackendMessage": "Your account has been created successfully!",
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=201)

    except Exception as e:
        return Response({
            "ofBackendMessage": "An unexpected error occurred while creating the account.",
            "errorDetails": str(e)
        }, status=400)


# Login User
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    """
    Login a user and return tokens with user data
    """
    try:
        data = request.data
        username = data.get('email')  # Using email as username
        password = data.get('password')

        if not username or not password:
            return Response(
                {"ofBackendMessage": "Email and password are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if not user:
            print(f"Failed login attempt for email: {username}")
            return Response(
                {"ofBackendMessage": "Invalid email or password. Please try again."},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Make sure user has a role
        if not user.role:
            user.role = 'regular'
            user.save()
            
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        print(f"Successful login for: {user.email} with role: {user.role}")
        
        # Return both serializer formats for compatibility
        user_data = UserSerializer(user).data

        return Response({
            "ofBackendMessage": "You have successfully logged in!",
            "access": str(access_token),
            "refresh": str(refresh),
            "user": user_data
        }, status=status.HTTP_200_OK)

    except Exception as e:
        print(f"Login error: {str(e)}")
        return Response({
            "ofBackendMessage": f"An error occurred while logging in: {str(e)}",
        }, status=status.HTTP_400_BAD_REQUEST)


# Get User Details (Authenticated User)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    return Response(CustomUserSerializer(user).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    """
    Get current user profile information, ensuring role is included
    """
    try:
        user = request.user
        serializer = UserSerializer(user)
        data = serializer.data
        
        # Ensure role field is included and defaults to 'regular' if not set
        if 'role' not in data or not data['role']:
            data['role'] = 'regular'
            
        # Log what data is being sent for debugging
        print(f"Sending user data: {data}")
            
        return Response(data)
    except Exception as e:
        print(f"Error in get_user_profile: {e}")
        return Response(
            {"ofBackendMessage": f"Failed to get user profile: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def register_user(request):
    """
    Register a new user with proper role assignment
    """
    try:
        data = request.data
        username = data.get('email')  # Using email as username
        password = data.get('password')
        email = data.get('email')
        name = data.get('name', '')
        
        # Set default role to 'regular' if not provided
        role = data.get('role', 'regular')
        
        # Only allow regular or enthusiast roles during registration
        # Admin role should be set by superuser only
        if role not in ['regular', 'enthusiast']:
            role = 'regular'
            
        # Check if user already exists
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                {"ofBackendMessage": "This email is already registered. Try logging in."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create the user with django's create_user to properly handle password hashing
        user = CustomUser.objects.create_user(
            username=username, 
            password=password, 
            email=email, 
            name=name,
            role=role
        )
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token
        
        print(f"Created user: {user.email} with role: {user.role}")
        
        # Return user data and tokens in the format expected by frontend
        return Response({
            "ofBackendMessage": "User registered successfully!",
            "user": UserSerializer(user).data,
            "access": str(access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        print(f"Registration error: {str(e)}")
        return Response(
            {"ofBackendMessage": f"Failed to register user: {str(e)}"},
            status=status.HTTP_400_BAD_REQUEST
        )
