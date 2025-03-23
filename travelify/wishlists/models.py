from django.db import models
from users.models import CustomUser
from destinations.models import Destination  # Updated app name

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="wishlists")
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name="wishlisted_by")
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'destination')  # Prevents duplicate wishlist entries for the same user

    def __str__(self):
        return f"{self.user.name} - {self.destination.name}"
