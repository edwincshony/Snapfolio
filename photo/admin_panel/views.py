from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import User
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import AdminUserCreationForm
from photographer.models import Portfolio
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from client.models import Booking
from django.db.models import Q
from .models import PlatformStatistics, PortfolioAnalytics, AdminNotification,UserActivityLog
from django.db.models import Count, Avg
from django.utils import timezone

def is_admin(user):
    return user.is_authenticated and user.userprofile.user_type == 'admin'

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get platform statistics
    total_users = User.objects.filter(is_active=True, is_superuser=False).count()
    total_photographers = User.objects.filter(userprofile__user_type='photographer').count()
    total_clients = User.objects.filter(userprofile__user_type='client').count()
    total_bookings = Booking.objects.count()
    total_portfolios = Portfolio.objects.count()
    
    # Save daily statistics
    PlatformStatistics.objects.create(
        total_users=total_users,
        total_photographers=total_photographers,
        total_clients=total_clients,
        total_bookings=total_bookings,
        total_portfolios=total_portfolios
    )
    
    # Get pending portfolios for approval
    pending_portfolios = Portfolio.objects.filter(is_approved=False)
    
    # Get recent notifications
    notifications = AdminNotification.objects.filter(is_read=False).order_by('-created_at')[:5]
    
    context = {
        'total_users': total_users,
        'total_photographers': total_photographers,
        'total_clients': total_clients,
        'total_bookings': total_bookings,
        'total_portfolios': total_portfolios,
        'pending_portfolios': pending_portfolios,
        'notifications': notifications
    }
    return render(request, 'admin_panel/dashboard.html', context)

@user_passes_test(is_admin)
def portfolio_approval(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            portfolio.is_approved = True
            portfolio.save()
            messages.success(request, f'Portfolio for {portfolio.photographer.username} has been approved.')
        elif action == 'reject':
            portfolio.delete()
            messages.success(request, f'Portfolio for {portfolio.photographer.username} has been rejected.')
        return redirect('admin_dashboard')
    
    # Handle GET request by rendering the approval template
    return render(request, 'admin_panel/portfolio_approval.html', {'portfolio': portfolio})

""" @user_passes_test(is_admin)
def user_management(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_panel/user_management.html', {'users': users}) """

@user_passes_test(is_admin)
def user_management(request):
    # Get query parameters from the request
    user_type = request.GET.get('user_type', '')
    search_query = request.GET.get('search', '')

    # Start with all users
    users = User.objects.all().order_by('-date_joined')

    # Apply filters based on user_type
    if user_type:
        users = users.filter(userprofile__user_type=user_type)

    # Apply search filter
    if search_query:
        users = users.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'users': users,
        'user_type': user_type,
        'search': search_query,
    }
    return render(request, 'admin_panel/user_management.html', context)

@user_passes_test(is_admin)
def toggle_user_status(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} has been {status}.')
    return redirect('user_management')

@user_passes_test(is_admin)
def analytics(request):
    # Get today's date
    today = timezone.now().date()
    
    # Get portfolio performance statistics
    portfolio_stats = Portfolio.objects.annotate(
        avg_rating=Avg('feedback__rating'),
        total_bookings=Count('bookings'),
        total_inquiries=Count('inquiries')
    )

    for portfolio in portfolio_stats:
        analytics_entry, created = PortfolioAnalytics.objects.get_or_create(
            portfolio=portfolio,
            date=today,
            defaults={
                'views': 0,  # Implement actual view tracking
                'inquiries': portfolio.total_inquiries,
                'bookings': portfolio.total_bookings,
                'average_rating': portfolio.avg_rating or 0.0
            }
        )

        # If the entry already exists, update the values instead of creating a new record
        if not created:
            analytics_entry.inquiries = portfolio.total_inquiries
            analytics_entry.bookings = portfolio.total_bookings
            analytics_entry.average_rating = portfolio.avg_rating or 0.0
            analytics_entry.save()

    context = {
        'portfolio_stats': portfolio_stats,
    }
    return render(request, 'admin_panel/analytics.html', context)



@user_passes_test(is_admin)
def notification_list(request):
    notifications = AdminNotification.objects.all().order_by('-created_at')
    return render(request, 'admin_panel/notifications.html', {'notifications': notifications})

@user_passes_test(is_admin)
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(AdminNotification, pk=notification_id)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')

@login_required
@staff_member_required
def approve_portfolio(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    portfolio.is_approved = True
    portfolio.save()
    messages.success(request, "Portfolio approved successfully.")
    return redirect('admin_dashboard')

@login_required
def user_activity_logs(request):
    logs = UserActivityLog.objects.all().order_by('-timestamp')
    return render(request, 'admin_panel/user_activity_logs.html', {'logs': logs})

@login_required
@user_passes_test(is_admin)
def admin_create_user(request):
    if request.method == "POST":
        form = AdminUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User created successfully!")
            return redirect('admin_user_list')  # Redirect to user list page
    else:
        form = AdminUserCreationForm()
    
    return render(request, 'admin_panel/admin_create_user.html', {'form': form})