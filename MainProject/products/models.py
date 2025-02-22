from django.db import models

# Define choices as a tuple of tuples
# AVAILABILITY_CHOICES = [
#     ('available', 'Available'),
#     ('not available', 'Not Available'),
# ]

# Create your model
class Product(models.Model):  # Class name should be capitalized as per Django convention
    profile_picture = models.ImageField(upload_to='media/products', blank=True, null=True)
    name = models.CharField(max_length=100)
    description = models.TextField()  # Increased max_length for better descriptions
    # availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')

    def __str__(self):
        return self.name  # Helps in identifying objects in the Django admin panel
