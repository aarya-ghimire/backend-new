from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('general_user', 'General User'),
        ('travel_enthusiast', 'Travel Enthusiast'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='general_user')
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(unique=True)
    

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['username']   
    
    def __str__(self):
        return self.email
