from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking, Inquiry
from .forms import BookingForm, InquiryForm, InquiryResponseForm
from photographer.models import Portfolio
from django.db.models import Q

def browse_portfolios(request):
    # Get the specialization filter from the query parameters
    specialization = request.GET.get('specialization', '')
    
    # Base queryset of approved portfolios
    portfolios = Portfolio.objects.filter(is_approved=True)
    
    # Apply specialization filter if selected
    if specialization:
        portfolios = portfolios.filter(specialization=specialization)
    
    # Order by most recently updated
    portfolios = portfolios.order_by('-updated_at')
    
    context = {
        'portfolios': portfolios,
        'specialization': specialization,
    }
    return render(request, 'client/browse_portfolios.html', context)

@login_required
def create_booking(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, is_approved=True)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.client = request.user
            booking.photographer = portfolio
            booking.save()
            messages.success(request, 'Booking request sent successfully!')
            return redirect('my_bookings')
    else:
        form = BookingForm()
    
    return render(request, 'client/create_booking.html', {
        'form': form,
        'portfolio': portfolio
    })

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client/my_bookings.html', {'bookings': bookings})

@login_required
def create_inquiry(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, pk=portfolio_id, is_approved=True)
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.client = request.user
            inquiry.photographer = portfolio
            inquiry.save()
            messages.success(request, 'Inquiry sent successfully!')
            return redirect('portfolio_detail', pk=portfolio_id)
    else:
        form = InquiryForm()
    
    return render(request, 'client/create_inquiry.html', {
        'form': form,
        'portfolio': portfolio
    })

@login_required
def my_inquiries(request):
    inquiries = Inquiry.objects.filter(client=request.user).order_by('-created_at')
    return render(request, 'client/my_inquiries.html', {'inquiries': inquiries})


@login_required
def edit_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, client=request.user)

    # Prevent editing if the inquiry is resolved or has a response
    if inquiry.is_resolved or inquiry.response:
        messages.warning(request, "You cannot edit this inquiry after it has been resolved or responded to.")
        return redirect('my_inquiries')

    if request.method == 'POST':
        form = InquiryForm(request.POST, instance=inquiry)
        if form.is_valid():
            form.save()
            messages.success(request, "Inquiry updated successfully!")
            return redirect('my_inquiries')
    else:
        form = InquiryForm(instance=inquiry)

    return render(request, 'client/edit_inquiry.html', {'form': form, 'inquiry': inquiry})


@login_required
def delete_inquiry(request, inquiry_id):
    inquiry = get_object_or_404(Inquiry, id=inquiry_id, client=request.user)

    # Prevent deleting if the inquiry is resolved
    if inquiry.is_resolved:
        messages.warning(request, "You cannot delete a resolved inquiry.")
        return redirect('my_inquiries')

    inquiry.delete()
    messages.success(request, "Inquiry deleted successfully!")
    return redirect('my_inquiries')


