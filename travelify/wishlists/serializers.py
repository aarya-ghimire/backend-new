from rest_framework import serializers
from .models import Wishlist
from destinations.models import Destination

class WishlistSerializer(serializers.ModelSerializer):
    destination_name = serializers.ReadOnlyField(source='destination.name')  # Read-only destination name
    user_name = serializers.ReadOnlyField(source='user.name')  # Read-only user name

    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'user_name', 'destination', 'destination_name', 'added_at']
        read_only_fields = ['id', 'added_at', 'user_name', 'destination_name']  # Prevents manual modifications
