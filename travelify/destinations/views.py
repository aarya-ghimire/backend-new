from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import Destination, Review
from .serializers import DestinationSerializer, ReviewSerializer

# Create a new destination or get all destinations
@api_view(['GET', 'POST'])
@permission_classes([AllowAny])  # Anyone can view, but only authenticated users can create
def destinations_list_create(request):
    if request.method == 'GET':
        destinations = Destination.objects.all()
        serializer = DestinationSerializer(destinations, many=True)
        return Response(serializer.data, status=200)

    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to add a destination."}, status=401)

        serializer = DestinationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "ofBackendMessage": "Destination added successfully!",
                "destination": serializer.data
            }, status=201)
        return Response(serializer.errors, status=400)


# Get, update, or delete a specific destination
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([AllowAny])  # Anyone can view, but only authenticated users can modify
def destination_detail(request, id):
    try:
        destination = Destination.objects.get(id=id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=404)

    if request.method == 'GET':
        serializer = DestinationSerializer(destination)
        return Response(serializer.data)

    elif request.method == 'PUT':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to update a destination."}, status=401)

        serializer = DestinationSerializer(destination, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "ofBackendMessage": "Destination updated successfully!",
                "destination": serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)

    elif request.method == 'DELETE':
        if not request.user.is_authenticated:
            return Response({"ofBackendMessage": "Authentication required to delete a destination."}, status=401)

        destination.delete()
        return Response({"ofBackendMessage": "Destination deleted successfully."}, status=200)


# Create a review for a destination
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_review(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=404)

    data = request.data
    serializer = ReviewSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save(user=request.user, destination=destination)
        return Response({
            "ofBackendMessage": "Review added successfully!",
            "review": serializer.data
        }, status=201)
    return Response(serializer.errors, status=400)


# Get all reviews for a specific destination
@api_view(['GET'])
@permission_classes([AllowAny])
def get_reviews(request, destination_id):
    try:
        destination = Destination.objects.get(id=destination_id)
    except Destination.DoesNotExist:
        return Response({"ofBackendMessage": "Destination not found."}, status=404)

    reviews = Review.objects.filter(destination=destination)
    serializer = ReviewSerializer(reviews, many=True)
    return Response(serializer.data, status=200)
