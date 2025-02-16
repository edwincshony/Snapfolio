from .models import Portfolio
from django import forms
from django.contrib.auth.models import User
from user_management.models import UserProfile  # Ensure correct import path
from django.contrib.auth.forms import UserCreationForm


class PortfolioApprovalForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ['is_approved']

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from user_management.models import UserProfile  # Ensure correct import

class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(choices=[
        ('photographer', 'Photographer'),
        ('client', 'Client'),
        ('admin', 'Admin')
    ])
    phone_number = forms.CharField(max_length=15, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'profile_picture')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():  # Check if email already exists
            raise ValidationError("A user with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)  # Save user instance but don't commit yet
        user.email = self.cleaned_data['email']

        if commit:
            user.save()  # Now save the user

            # Ensure the profile is created only if it doesn't exist
            user_profile, created = UserProfile.objects.get_or_create(user=user)
            user_profile.user_type = self.cleaned_data['user_type']
            user_profile.phone_number = self.cleaned_data['phone_number']
            if self.cleaned_data['profile_picture']:  # Only update if a new picture is uploaded
                user_profile.profile_picture = self.cleaned_data['profile_picture']
            user_profile.save()  # Save the updated profile

        return user
