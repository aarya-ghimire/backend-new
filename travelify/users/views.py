from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from .serializers import CustomUserSerializer

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
    try:
        data = request.data
        username = data.get('email')  # Using email as username
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
            return Response({"ofBackendMessage": "Invalid email or password. Please try again."}, status=400)

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "ofBackendMessage": "You have successfully logged in!",
            "access": str(access_token),
            "refresh": str(refresh),
            "user": CustomUserSerializer(user).data
        }, status=200)

    except Exception as e:
        return Response({
            "ofBackendMessage": "An error occurred while logging in. Please try again later.",
            "errorDetails": str(e)
        }, status=400)


# Get User Details (Authenticated User)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    return Response(CustomUserSerializer(user).data)
