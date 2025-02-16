from django import forms
from .models import Booking, Inquiry

class BookingForm(forms.ModelForm):
    event_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    
    class Meta:
        model = Booking
        fields = ['event_date', 'event_type', 'location', 'description']

class InquiryForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['subject', 'message']

class InquiryResponseForm(forms.ModelForm):
    class Meta:
        model = Inquiry
        fields = ['response']
