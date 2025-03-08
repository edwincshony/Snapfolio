from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Portfolio, Image, ClientFeedback
from client.models import Booking  # Import the Booking model
from .forms import PortfolioForm, ImageForm, ClientFeedbackForm, PhotographerResponseForm
from django.contrib.auth.models import User

# Create your views here.

@login_required
def create_portfolio(request):
    if Portfolio.objects.filter(photographer=request.user).exists():
        return redirect('edit_portfolio')

    if request.method == 'POST':
        form = PortfolioForm(request.POST)
        if form.is_valid():
            portfolio = form.save(commit=False)
            portfolio.photographer = request.user
            portfolio.save()
            messages.success(request, 'Portfolio created successfully!')
            return redirect('portfolio_detail', pk=portfolio.pk)
    else:
        form = PortfolioForm()

    return render(request, 'photographer/create_portfolio.html', {'form': form})


@login_required
def edit_portfolio(request):
    portfolio = get_object_or_404(Portfolio, photographer=request.user)
    if request.method == 'POST':
        form = PortfolioForm(request.POST, instance=portfolio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Portfolio updated successfully!')
            return redirect('portfolio_detail', pk=portfolio.pk)
    else:
        form = PortfolioForm(instance=portfolio)
    return render(request, 'photographer/edit_portfolio.html', {'form': form})

@login_required
def upload_image(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk, photographer=request.user)
    print("✅ Portfolio ID:", portfolio.id)  # Debugging

    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.portfolio = portfolio  # Assign to correct portfolio
            image.save()
            messages.success(request, '✅ Image uploaded successfully!')

            return redirect('portfolio_detail', pk=portfolio.pk)  # Redirect correctly

    else:
        form = ImageForm()

    return render(request, 'photographer/upload_image.html', {'form': form, 'portfolio': portfolio})


def portfolio_detail(request, pk):
    portfolio = get_object_or_404(Portfolio, pk=pk)
    images = portfolio.images.all()
    feedback = portfolio.feedback.all()
    
    if request.method == 'POST' and request.user.is_authenticated:
        feedback_form = ClientFeedbackForm(request.POST)
        if feedback_form.is_valid():
            feedback = feedback_form.save(commit=False)
            feedback.portfolio = portfolio
            feedback.client = request.user
            feedback.save()
            messages.success(request, 'Feedback submitted successfully!')
            return redirect('portfolio_detail', pk=pk)
    else:
        feedback_form = ClientFeedbackForm()
    
    context = {
        'portfolio': portfolio,
        'images': images,
        'feedback': feedback,
        'feedback_form': feedback_form
    }
    return render(request, 'photographer/portfolio_detail.html', context)

@login_required
def respond_to_feedback(request, feedback_id):
    feedback = get_object_or_404(ClientFeedback, pk=feedback_id)
    if request.user != feedback.portfolio.photographer:
        messages.error(request, 'You are not authorized to respond to this feedback.')
        return redirect('portfolio_detail', pk=feedback.portfolio.pk)
    
    if request.method == 'POST':
        form = PhotographerResponseForm(request.POST, instance=feedback)
        if form.is_valid():
            form.save()
            messages.success(request, 'Response submitted successfully!')
            return redirect('portfolio_detail', pk=feedback.portfolio.pk)
    else:
        form = PhotographerResponseForm(instance=feedback)
    
    return render(request, 'photographer/respond_to_feedback.html', {
        'form': form,
        'feedback': feedback
    })

@login_required
def edit_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    # Check if the user owns this image
    if image.portfolio.photographer != request.user:
        messages.error(request, "You don't have permission to edit this image.")
        return redirect('portfolio_detail', pk=image.portfolio.id)
    
    if request.method == 'POST':
        # Update image details
        image.title = request.POST.get('title')
        image.description = request.POST.get('description')
        image.category = request.POST.get('category')
        image.save()
        
        messages.success(request, 'Image details updated successfully.')
        return redirect('portfolio_detail', pk=image.portfolio.id)
    
    return redirect('portfolio_detail', pk=image.portfolio.id)

@login_required
def delete_image(request, image_id):
    image = get_object_or_404(Image, id=image_id)
    
    # Check if the user owns this image
    if image.portfolio.photographer != request.user:
        messages.error(request, "You don't have permission to delete this image.")
        return redirect('portfolio_detail', pk=image.portfolio.id)
    
    if request.method == 'POST':
        portfolio_id = image.portfolio.id
        # Delete the image file
        image.image.delete()
        # Delete the image record
        image.delete()
        
        messages.success(request, 'Image deleted successfully.')      
        return redirect('portfolio_detail', pk=portfolio_id)
    
    return redirect('portfolio_detail', pk=image.portfolio.id)


@login_required
def photographer_bookings(request):
    """View for photographers to manage their bookings."""
    portfolio = get_object_or_404(Portfolio, photographer=request.user)
    bookings = Booking.objects.filter(photographer=portfolio).order_by('-created_at')
    return render(request, 'photographer/photographer_bookings.html', {'bookings': bookings})

@login_required
def update_booking_status(request, booking_id):
    """Allows photographers to update the status of bookings."""
    booking = get_object_or_404(Booking, id=booking_id, photographer__photographer=request.user)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['pending', 'confirmed', 'completed', 'canceled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f'Booking status updated to {new_status.capitalize()}.')
        else:
            messages.error(request, 'Invalid status selection.')

    return redirect('photographer_bookings')


