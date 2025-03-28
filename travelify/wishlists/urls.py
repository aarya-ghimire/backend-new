from django.urls import path
from .views import get_wishlist, add_to_wishlist, remove_from_wishlist

urlpatterns = [
    path('get/', get_wishlist, name='get_wishlist'),
    path('add/', add_to_wishlist, name='add_to_wishlist'),
    path('remove/<int:destination_id>/', remove_from_wishlist, name='remove_from_wishlist'),
]
