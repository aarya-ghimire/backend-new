from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from .models import Destination, Review, Category  # Import all models
from .serializers import DestinationSerializer, ReviewSerializer, CategorySerializer


# Create a new destination or get all destinations
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Anyone can view, but only authenticated users can create
def destinations_list_create(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to add a destination."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            # Set the 'user' field to the current authenticated user
            serializer.save(user=request.user)
            return Response({
                "ofBackendMessage": "Destination added successfully!",
                "destination": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Get, update, or delete a specific destination
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Anyone can view, but only authenticated users can modify
def destination_detail(request, id):
    try:
        destination = Destination.objects.get(id=id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to update a destination."}, status=status.HTTP_401_UNAUTHORIZED)

        if destination.user != request.user:
            return Response({"ofBackendMessage": "You can only update your own destinations."}, status=status.HTTP_403_FORBIDDEN)

        serializer = DestinationSerializer(destination, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "ofBackendMessage": "Destination updated successfully!",
                "destination": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to delete a destination."}, status=status.HTTP_401_UNAUTHORIZED)

        if destination.user != request.user:
            return Response({"ofBackendMessage": "You can only delete your own destinations."}, status=status.HTTP_403_FORBIDDEN)

        destination.delete()
        return Response({"ofBackendMessage": "Destination deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

    data = request.data.copy()  # Copy request data to modify it
    data['destination'] = destination.id  # Set the destination automatically

    serializer = ReviewSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(user=request.user, destination=destination)  # Save with user and destination
        return Response({
            "ofBackendMessage": "Review added successfully!",
            "review": serializer.data
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Get all reviews for a specific destination
@api_view(['GET'])
@permission_classes([AllowAny])
def get_reviews(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)

    reviews = Review.objects.filter(destination=destination)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_review(request, review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return Response({"ofBackendMessage": "Review not found."}, status=status.HTTP_404_NOT_FOUND)

    if review.user != request.user:
        return Response({"ofBackendMessage": "You can only edit your own reviews."}, status=status.HTTP_403_FORBIDDEN)

    serializer = ReviewSerializer(review, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "ofBackendMessage": "Review updated successfully!",
            "review": serializer.data
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Anyone can view, but only authenticated users can create
def category_list_create(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to add a category."}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "ofBackendMessage": "Category added successfully!",
                "category": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
