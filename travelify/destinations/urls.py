from django.urls import path
from .views import destinations_list_create, destination_detail, add_review, get_reviews,category_list_create, edit_review   


urlpatterns = [
    path('', destinations_list_create, name='destinations-list-create'),  
    path('<int:id>/', destination_detail, name='destination-detail'),  
    path('<int:destination_id>/reviews/', get_reviews, name='get-reviews'),  
    path('<int:destination_id>/add-review/', add_review, name='add-review'),  
    path('reviews/edit/<int:review_id>/', edit_review, name='edit_review'),
    path('categories/', category_list_create, name='categories-list-create'),  
]
