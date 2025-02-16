from django.urls import path
from django.contrib.admin.views.decorators import staff_member_required
from . import views



urlpatterns = [
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('portfolio-approval/<int:portfolio_id>/', views.portfolio_approval, name='portfolio_approval'),
    path('user-management/', views.user_management, name='user_management'),
    path('toggle-user/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    path('analytics/', views.analytics, name='analytics'),
    path('notifications/', views.notification_list, name='notification_list'),
    path('mark-notification-read/<int:notification_id>/', views.mark_notification_read, name='mark_notification_read'),

    path('admin_panel/approve-portfolio/<int:portfolio_id>/', views.approve_portfolio, name='approve_portfolio'),
    path('admin_panel/user-activity/', views.user_activity_logs, name='user_activity_logs'),

    path('admin_panel/create-user/', views.admin_create_user, name='admin_create_user'),


 ]
