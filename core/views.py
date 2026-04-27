# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  Views
#  File: core/views.py  (REPLACE the whole file)
# =====================================================

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Service, Review, DailyMessage
from .forms import BookingForm, ReviewForm, ContactForm, RegisterForm
from django.db import IntegrityError
from datetime import date


# ─── DAILY MESSAGES ───────────────────────────────────────────────
DAILY_MESSAGES = [
    "Trust the ancestors — your path is guided by those who loved you before time.",
    "Healing begins within your spirit; still the noise and listen to what is ancient.",
    "You are protected and aligned with your purpose. Walk without fear today.",
    "Peace flows through you like the sacred river — clear, constant, unstoppable.",
    "Your journey is sacred. Every step, even the uncertain ones, has been blessed.",
    "The bones do not lie. What is meant for you will find you in its season.",
    "You were not given this life to carry it alone. Your ancestors stand beside you.",
    "Like the mountain, you have survived every storm that came before this one.",
    "The sunrise does not ask permission — neither should your healing begin today.",
    "Be still as the cave in darkness; wisdom lives in the quiet, not the noise.",
    "Your roots go deeper than your pain. Draw strength from all who came before.",
    "Even the ocean, vast and powerful, knows when to be calm. So too can your heart.",
    "What grows in the wild places was not planted by human hands — so too your spirit.",
    "The stars remember every name. Yours has been spoken in the heavens since before.",
    "Flowers bloom in cracked earth. From your brokenness, something sacred will rise.",
    "Stone endures what water cannot hold. Your endurance is your greatest medicine.",
    "Walk softly upon this earth — she holds the bones of those who guide you still.",
    "A new day is not just a beginning; it is an answered prayer from the night before.",
    "You have ancestors who faced fires darker than yours, and still they sang. So can you.",
    "The clouds part for no one, yet the sun always waits patiently behind them. So does joy.",
    "To know yourself is the beginning of all wisdom — start there, today, without rushing.",
    "Let the river teach you: it does not fight its banks. It finds its way around every obstacle.",
    "In the silence after prayer, the ancestors lean in close. Be still enough to hear them.",
    "Your calling was written before your birth. You are not lost — you are still arriving.",
    "Every tree you see began as something that could be crushed underfoot. Remember this.",
    "The night is not against you. It is preparing you for a morning you have not yet imagined.",
    "Tend your inner world as you would a sacred fire — with patience, care, and intention.",
    "What the eyes cannot see, the spirit knows. Trust your deep knowing today.",
    "You are the harvest of generations of prayers and endurance. Do not forget your worth.",
    "Today, breathe. Tomorrow will come whether or not you carry its weight today.",
]


def get_daily_message():
    latest = DailyMessage.objects.filter(active=True).order_by('-created_at').first()
    if latest:
        return latest.text

    today = date.today()
    day_of_year = today.timetuple().tm_yday
    return DAILY_MESSAGES[day_of_year % len(DAILY_MESSAGES)]


# ─── HOME ──────────────────────────────────────────────────────────
def home(request):
    services = Service.objects.all()
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {
        'services': services,
        'reviews': reviews,
        'daily_message': get_daily_message(),
    })


# ─── ABOUT ─────────────────────────────────────────────────────────
def about(request):
    return render(request, 'core/about.html', {
        'about_text': None,
    })


# ─── SERVICES ──────────────────────────────────────────────────────
def services(request):
    return render(request, 'core/services.html', {
        'services': Service.objects.all(),
    })


# ─── BOOK ──────────────────────────────────────────────────────────
def book(request):
    message = ""
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                message = "✅ Your appointment has been booked successfully!"
                form = BookingForm()
            except IntegrityError:
                message = "❌ This date is already booked for that service."
    else:
        form = BookingForm()
    return render(request, 'core/book.html', {'form': form, 'message': message})


# ─── REVIEW ────────────────────────────────────────────────────────
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


# ─── CONTACT ───────────────────────────────────────────────────────
def contact(request):
    message = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = "✅ Your message has been sent. We will be in touch soon."
            form = ContactForm()
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form, 'message': message})


# ─── LOCATION ──────────────────────────────────────────────────────
def location(request):
    return render(request, 'core/location.html')


# ─── REGISTER ──────────────────────────────────────────────────────
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})


# ─── LOGIN ─────────────────────────────────────────────────────────
def user_login(request):
    message = ""
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
        else:
            message = "❌ Invalid credentials. Please try again."
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form, 'message': message})


# ─── LOGOUT ────────────────────────────────────────────────────────
def user_logout(request):
    logout(request)
    return redirect('home')