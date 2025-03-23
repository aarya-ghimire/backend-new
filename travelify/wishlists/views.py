from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Wishlist
from destinations.models import Destination
from .serializers import WishlistSerializer

# Get all wishlist items for authenticated user
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request):
    wishlists = Wishlist.objects.filter(user=request.user)
    serializer = WishlistSerializer(wishlists, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

# Add a destination to wishlist
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_wishlist(request):
    try:
        destination_id = request.data.get("destination_id")
        destination = Destination.objects.get(id=destination_id)

        # Check if already in wishlist
        if Wishlist.objects.filter(user=request.user, destination=destination).exists():
            return Response({"message": "Destination is already in your wishlist."}, status=status.HTTP_400_BAD_REQUEST)

        wishlist_item = Wishlist.objects.create(user=request.user, destination=destination)
        serializer = WishlistSerializer(wishlist_item)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Destination.DoesNotExist:
        return Response({"message": "Destination not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Remove a destination from wishlist
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_wishlist(request, destination_id):
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, destination_id=destination_id)
        wishlist_item.delete()
        return Response({"message": "Destination removed from wishlist."}, status=status.HTTP_204_NO_CONTENT)
    except Wishlist.DoesNotExist:
        return Response({"message": "Destination not found in wishlist."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
