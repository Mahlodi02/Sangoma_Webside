# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  Views
#  File: core/views.py  (REPLACE the whole file)
# =====================================================

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .models import Service, Review, DailyMessage, DailyMessageComment
from .forms import BookingForm, ReviewForm, ContactForm, RegisterForm, DailyMessageCommentForm
from django.db import IntegrityError


# ─── DAILY MESSAGES ───────────────────────────────────────────────
def get_daily_message():
    latest = DailyMessage.objects.filter(active=True).order_by('-created_at').first()
    return latest.text if latest else 'Lesedi'


# ─── HOME ──────────────────────────────────────────────────────────
def home(request):
    services = Service.objects.all()
    reviews = Review.objects.all().order_by('-created_at')
    daily_message_obj = DailyMessage.objects.filter(active=True).order_by('-created_at').first()
    daily_message = (daily_message_obj.text if daily_message_obj else 'Lesedi') if request.user.is_authenticated else None
    daily_message_comments = daily_message_obj.comments.all() if request.user.is_authenticated and daily_message_obj else []
    comment_message = ''

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        if daily_message_obj:
            comment_form = DailyMessageCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.daily_message = daily_message_obj
                comment.user = request.user
                comment.save()
                comment_message = '✅ Your comment has been posted. Thank you for sharing encouragement.'
                comment_form = DailyMessageCommentForm()
        else:
            comment_form = None
    else:
        comment_form = DailyMessageCommentForm() if request.user.is_authenticated and daily_message_obj else None

    return render(request, 'core/home.html', {
        'services': services,
        'reviews': reviews,
        'daily_message': daily_message,
        'daily_message_obj': daily_message_obj,
        'daily_message_comments': daily_message_comments,
        'comment_form': comment_form,
        'comment_message': comment_message,
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