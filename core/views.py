from django.shortcuts import render
from .models import Service, Review
from django.db import IntegrityError
from .forms import BookingForm
from .forms import ReviewForm
import random
from datetime import date

def home(request):
    services = Service.objects.all()
    reviews = Review.objects.all().order_by('-created_at')

    messages = [
        "Trust the ancestors, your path is guided.",
        "Healing begins within your spirit.",
        "You are protected and aligned with your purpose.",
        "Peace flows through you like the river.",
        "Your journey is sacred, trust it."
    ]

    today_index = date.today().day % len(messages)
    daily_message = messages[today_index]

    return render(request, 'core/home.html', {
        'services': services,
        'reviews': reviews,
        'daily_message': daily_message
    })

def book(request):
    message = ""

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                message = "✅ Your appointment has been booked successfully!"
                form = BookingForm()  # clears form after success
            except IntegrityError:
                message = "❌ This date is already booked for that service."
    else:
        form = BookingForm()

    return render(request, 'core/book.html', {'form': form, 'message': message})

def services(request):
    services = Service.objects.all()
    return render(request, 'core/services.html', {'services': services})


def review(request):
    message = ""

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            message = "✅ Thank you for your review!"
            form = ReviewForm()
    else:
        form = ReviewForm()

    return render(request, 'core/review.html', {'form': form, 'message': message})
