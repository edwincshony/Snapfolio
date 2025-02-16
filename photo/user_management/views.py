from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg
from django.urls import reverse
from .forms import SignUpForm, UserProfileUpdateForm, UserUpdateForm,LoginForm
from photographer.models import Portfolio
from .models import UserProfile
from django.contrib.auth.models import User

# Create your views here.

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.userprofile.phone_number = form.cleaned_data.get('phone_number')
            user.userprofile.user_type = form.cleaned_data.get('user_type')
            if form.cleaned_data.get('profile_picture'):
                user.userprofile.profile_picture = form.cleaned_data.get('profile_picture')
            user.userprofile.save()
            
            # Redirect to login page after successful signup
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('login')  # Redirect to the login page
    else:
        form = SignUpForm()
    return render(request, 'user_management/signup.html', {'form': form})

def login_view(request):
    next_url = request.GET.get('next')  # Get the "next" parameter from the URL
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                # Ensure the user has a UserProfile
                try:
                    user_profile = user.userprofile
                except UserProfile.DoesNotExist:
                    # Create a UserProfile if it doesn't exist
                    UserProfile.objects.create(user=user)

                auth_login(request, user)
                print(f"User {user.username} - Superuser: {user.is_superuser}")  # Debugging

                # Redirect to 'next' URL if it exists, otherwise redirect based on user type
                if next_url:
                    return redirect(next_url)
                elif user.is_superuser:
                    return redirect(reverse('admin_dashboard'))  # Ensure this is the correct name
                else:
                    return redirect(reverse('home'))
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid input. Please check your credentials.')
    else:
        form = LoginForm()
    return render(request, 'user_management/login.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileUpdateForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'user_management/profile.html', context)

def home(request):
    # Get featured portfolios (approved portfolios with highest ratings)
    featured_portfolios = Portfolio.objects.filter(
        is_approved=True
    ).annotate(
        avg_rating=Avg('feedback__rating')
    ).order_by('-avg_rating')[:3]
    
    return render(request, 'user_management/home.html', {
        'featured_portfolios': featured_portfolios
    })


def logout_view(request):
    logout(request)
    return redirect('/login/')
