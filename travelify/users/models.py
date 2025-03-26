from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class CustomUser(AbstractUser):
    # Role choices aligned with frontend expectations
    ROLE_CHOICES = (
        ('regular', 'Regular User'),
        ('enthusiast', 'Travel Enthusiast'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='regular')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']   
    
    def __str__(self):
        return self.email
        
    def get_token(self):
        """
        Generate JWT token for this user
        """
        refresh = RefreshToken.for_user(self)
        return str(refresh.access_token)
