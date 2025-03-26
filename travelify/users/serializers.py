from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'password', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserSerializer(serializers.ModelSerializer):
    """
    Extended serializer for user data with proper role handling
    """
    class Meta:
        model = CustomUser
        fields = ['id', 'name', 'email', 'role']
        
    def to_representation(self, instance):
        """
        Ensure role is always included in the representation
        """
        data = super().to_representation(instance)
        # Default to 'regular' if role is not set
        if 'role' not in data or not data['role']:
            data['role'] = 'regular'
        return data
