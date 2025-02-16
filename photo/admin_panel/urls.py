from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portfolio-approval/<int:portfolio_id>/', views.portfolio_approval, name='portfolio_approval'),
    path('user-management/', views.user_management, name='user_management'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('analytics/', views.analytics, name='analytics'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),
]
