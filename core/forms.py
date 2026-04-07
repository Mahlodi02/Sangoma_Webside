from django import forms
from .models import Booking, Review
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

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