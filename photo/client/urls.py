from django.urls import path
from . import views

urlpatterns = [
    path('browse/', views.browse_portfolios, name='browse_portfolios'),
    path('book/<int:portfolio_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('inquire/<int:portfolio_id>/', views.create_inquiry, name='create_inquiry'),
    path('my-inquiries/', views.my_inquiries, name='my_inquiries'),
]
