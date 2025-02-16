from django.db import models
from django.contrib.auth.models import User
from photographer.models import Portfolio

# Create your models here.

class PlatformStatistics(models.Model):
    date = models.DateField(auto_now_add=True)
    total_users = models.IntegerField(default=0)
    total_photographers = models.IntegerField(default=0)
    total_clients = models.IntegerField(default=0)
    total_bookings = models.IntegerField(default=0)
    total_portfolios = models.IntegerField(default=0)
    active_users = models.IntegerField(default=0)

    class Meta:
        verbose_name_plural = "Platform Statistics"

    def __str__(self):
        return f"Statistics for {self.date}"

class PortfolioAnalytics(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='analytics')
    date = models.DateField(auto_now_add=True)
    views = models.IntegerField(default=0)
    inquiries = models.IntegerField(default=0)
    bookings = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    class Meta:
        verbose_name_plural = "Portfolio Analytics"
        unique_together = ('portfolio', 'date')

    def __str__(self):
        return f"Analytics for {self.portfolio.photographer.username} on {self.date}"

class AdminNotification(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=[
        ('portfolio_approval', 'Portfolio Approval Request'),
        ('user_report', 'User Report'),
        ('system_alert', 'System Alert')
    ])
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    related_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.notification_type}: {self.title}"
