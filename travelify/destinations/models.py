from django.db import models
from users.models import CustomUser  

# Destination Model
class Destination(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    location = models.CharField(max_length=255)
    country = models.CharField(max_length=100)
    best_time_to_visit = models.CharField(max_length=100)
    activities = models.TextField()
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='destination_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    # Optionally add a method to update fields like rating or image if needed
    def update_fields(self, name=None, description=None, location=None, country=None,
                      best_time_to_visit=None, activities=None, average_cost=None, rating=None, image=None):
        if name:
            self.name = name
        if description:
            self.description = description
        if location:
            self.location = location
        if country:
            self.country = country
        if best_time_to_visit:
            self.best_time_to_visit = best_time_to_visit
        if activities:
            self.activities = activities
        if average_cost:
            self.average_cost = average_cost
        if rating is not None:
            self.rating = rating
        if image:
            self.image = image
        self.save()

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Review Model
class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1 to 5 rating
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.name} on {self.destination.name}"
