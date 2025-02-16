from django.db import models
from django.contrib.auth.models import User

class Portfolio(models.Model):
    SPECIALIZATION_CHOICES = [
        ('portrait', 'Portrait Photography'),
        ('wedding', 'Wedding Photography'),
        ('landscape', 'Landscape Photography'),
        ('fashion', 'Fashion Photography'),
        ('wildlife', 'Wildlife Photography'),
    ]

    photographer = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    specialization = models.CharField(max_length=20, choices=SPECIALIZATION_CHOICES)
    experience = models.IntegerField(help_text="Years of experience")
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.photographer.username}'s Portfolio"

class Image(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='portfolio_images/')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.portfolio.photographer.username}"

class ClientFeedback(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='feedback')
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    photographer_response = models.TextField(blank=True)

    class Meta:
        unique_together = ('portfolio', 'client')

    def __str__(self):
        return f"Feedback from {self.client.username} for {self.portfolio.photographer.username}"
