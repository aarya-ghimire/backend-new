from django.urls import path
from .views import create_user, login_user, get_user_details

urlpatterns = [
    path('register/', create_user, name='register'),
    path('login/', login_user, name='login'),
    path('me/', get_user_details, name='user-details'),
]
