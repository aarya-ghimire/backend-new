from rest_framework import serializers
from .models import Destination, Category, Review

class DestinationSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)  # Ensure image field provides full URL

    class Meta:
        model = Destination
        fields = '__all__'  # Includes all fields

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)  # Display user name
    destination_name = serializers.CharField(source="destination.name", read_only=True)  # Display destination name

    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'destination', 'destination_name', 'rating', 'comment', 'created_at']
        read_only_fields = ['user', 'created_at']  # user and timestamp should not be modified
