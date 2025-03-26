from django.urls import path
from .views import register_user, login_user, get_user_details, get_user_profile

urlpatterns = [
    path('register/', register_user, name='register'),
    path('login/', login_user, name='login'),
    path('me/', get_user_details, name='get_user_details'),
    path('profile/', get_user_profile, name='get_user_profile'),
]
