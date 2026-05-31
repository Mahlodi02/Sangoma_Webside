# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  Forms
#  File: core/forms.py  (REPLACE the whole file)
# =====================================================

from django import forms
from .models import Booking, Review, DailyMessageComment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name  = forms.CharField(required=False)
    email      = forms.EmailField(required=True)
    phone      = forms.CharField(required=False)

    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user            = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name  = self.cleaned_data['last_name']
        user.email      = self.cleaned_data['email']
        if commit:
            user.save()
            # Save phone to Profile (create/update)
            phone = self.cleaned_data.get('phone', '').strip()
            try:
                # import here to avoid circular imports at module import time
                from accounts.models import Profile
                if phone:
                    Profile.objects.update_or_create(user=user, defaults={'phone': phone})
                else:
                    # ensure profile exists
                    Profile.objects.get_or_create(user=user)
            except Exception:
                # If accounts app isn't available for some reason, ignore and continue
                pass
        return user


class BookingForm(forms.ModelForm):
    class Meta:
        model   = Booking
        fields  = ['name', 'service', 'date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.date.today().isoformat()
            })
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model  = Review
        fields = ['name', 'message', 'rating']


class ContactForm(forms.Form):
    name    = forms.CharField(max_length=100)
    email   = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class DailyMessageCommentForm(forms.ModelForm):
    class Meta:
        model   = DailyMessageComment
        fields  = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Write a positive thought or encouragement for others...'
            })
        }