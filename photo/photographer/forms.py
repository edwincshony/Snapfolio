from django import forms
from .models import Portfolio, Image, ClientFeedback

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['title', 'description', 'specialization', 'experience']

class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'title', 'description', 'category']

class ClientFeedbackForm(forms.ModelForm):
    class Meta:
        model = ClientFeedback
        fields = ['rating', 'comment']

class PhotographerResponseForm(forms.ModelForm):
    class Meta:
        model = ClientFeedback
        fields = ['photographer_response']
