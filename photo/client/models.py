from django.db import models
from django.contrib.auth.models import User
from photographer.models import Portfolio

# Create your models here.

class Booking(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    photographer = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='bookings')
    event_date = models.DateField()
    event_type = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.client.username} with {self.photographer.photographer.username}"

class Inquiry(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    photographer = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='inquiries')
    subject = models.CharField(max_length=200)
    message = models.TextField()
    response = models.TextField(blank=True)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Inquiry from {self.client.username} to {self.photographer.photographer.username}"





