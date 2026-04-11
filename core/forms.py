# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  Forms
#  File: core/forms.py  (REPLACE the whole file)
# =====================================================

from django import forms
from .models import Booking, Review
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'service', 'date']
        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'min': datetime.date.today().isoformat()
            })
        }


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['name', 'message', 'rating']


class ContactForm(forms.Form):
    name    = forms.CharField(max_length=100)
    email   = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)