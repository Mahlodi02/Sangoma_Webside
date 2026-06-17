# =====================================================
#  Ntatemoholo Seromo — Sangoma Wisdom
#  Views
#  File: core/views.py  (REPLACE the whole file)
# =====================================================
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Service, Review, DailyMessage, DailyMessageComment
from .forms import BookingForm, ReviewForm, ContactForm, RegisterForm, EmailAuthenticationForm, DailyMessageCommentForm
from django.db import IntegrityError
import json
from django.contrib import messages


# ─── HOME ──────────────────────────────────────────────────────────
def home(request):
    services      = Service.objects.all()
    reviews       = Review.objects.all().order_by('-created_at')
    latest_msg    = DailyMessage.objects.filter(active=True).first()
    daily_message = latest_msg.text if latest_msg else "The ancestors are preparing today's message. Check back soon. ✦"
    daily_message_comments = []
    comment_form = None
    if request.user.is_authenticated and latest_msg:
        if request.method == 'POST':
            comment_form = DailyMessageCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.daily_message = latest_msg
                comment.user = request.user
                comment.save()
                messages.success(request, '✅ Your encouragement has been posted.')
                return redirect('home')
        else:
            comment_form = DailyMessageCommentForm()
        daily_message_comments = latest_msg.comments.all().order_by('-created_at')
    return render(request, 'core/home.html', {
        'services':      services,
        'reviews':       reviews,
        'daily_message': daily_message,
        'latest_msg':    latest_msg,
        'daily_message_comments': daily_message_comments,
        'comment_form': comment_form,
    })


# ─── ABOUT ─────────────────────────────────────────────────────────
def about(request):
    return render(request, 'core/about.html', {'about_text': None})


# ─── SERVICES ──────────────────────────────────────────────────────
def services(request):
    return render(request, 'core/services.html', {
        'services': Service.objects.all(),
    })


# ─── BOOK ──────────────────────────────────────────────────────────
def book(request):
    message = ''
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                message = '✅ Your appointment has been booked successfully!'
                form = BookingForm()
            except IntegrityError:
                message = '❌ This date is already booked for that service.'
    else:
        form = BookingForm()
    return render(request, 'core/book.html', {'form': form, 'message': message})


# ─── REVIEW ────────────────────────────────────────────────────────
def review(request):
    message = ''
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            message = '✅ Thank you for your review!'
            form = ReviewForm()
    else:
        form = ReviewForm()
    return render(request, 'core/review.html', {'form': form, 'message': message})


# ─── CONTACT ───────────────────────────────────────────────────────
def contact(request):
    message = ''
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = '✅ Your message has been sent. We will be in touch soon.'
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
            # Use POST-Redirect-GET and Django messages so success reliably appears
            registered_name = user.first_name or user.username
            messages.success(request, f"✅ Account created successfully! Welcome, {registered_name}.")
            return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

# ─── LOGIN ─────────────────────────────────────────────────────────
def user_login(request):
    message = ''
    if request.method == 'POST':
        form = EmailAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
        else:
            message = '❌ Invalid login. Use your email or username and password.'
    else:
        form = EmailAuthenticationForm(request)
    return render(request, 'core/login.html', {'form': form, 'message': message})

# ─── LOGOUT ────────────────────────────────────────────────────────
def user_logout(request):
    logout(request)
    return redirect('home')


# ═══════════════════════════════════════════════════════════════════
# DAILY MESSAGE FEED — Facebook-style (login required)
# ═══════════════════════════════════════════════════════════════════

@login_required(login_url='login')
def daily_messages_feed(request):
    from .models import MessageReaction

    messages_list = DailyMessage.objects.filter(active=True)
    reaction_emojis = ['❤️', '🙏', '✨', '😢', '🔥']
    for msg in messages_list:
        try:
            msg.user_reaction = MessageReaction.objects.get(
                daily_message=msg, user=request.user
            ).emoji
        except MessageReaction.DoesNotExist:
            msg.user_reaction = None
        msg.comment_count  = msg.comments.count()
        msg.total_reactions = msg.reactions.count()
        msg.emoji_counts = {
            emoji: msg.reactions.filter(emoji=emoji).count()
            for emoji in reaction_emojis
        }
        msg.share_count = msg.shares.count() if hasattr(msg, 'shares') else 0
    return render(request, 'core/daily_messages_feed.html', {
        'messages_list': messages_list,
    })


# ─── SINGLE MESSAGE DETAIL with comments ───────────────────────────
@login_required(login_url='login')
def daily_message_detail(request, pk):
    msg      = get_object_or_404(DailyMessage, pk=pk)
    comments = msg.comments.all().order_by('-created_at')

    from .models import MessageReaction

    try:
        user_reaction = MessageReaction.objects.get(
            daily_message=msg, user=request.user
        ).emoji
    except MessageReaction.DoesNotExist:
        user_reaction = None

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            DailyMessageComment.objects.create(
                daily_message=msg,
                user=request.user,
                text=text,
            )
            return redirect('daily_message_detail', pk=pk)

    reaction_emojis = ['❤️', '🙏', '✨', '😢', '🔥']
    reaction_counts = {
        emoji: msg.reactions.filter(emoji=emoji).count()
        for emoji in reaction_emojis
    }

    share_count = msg.shares.count() if hasattr(msg, 'shares') else 0

    return render(request, 'core/daily_message_detail.html', {
        'msg':             msg,
        'comments':        comments,
        'user_reaction':   user_reaction,
        'reaction_counts': reaction_counts,
        'reaction_emojis': reaction_emojis,
        'total_reactions': msg.reactions.count(),
        'total_comments':  comments.count(),
        'share_count':     share_count,
    })


# ─── REACT TO MESSAGE (AJAX) ────────────────────────────────────────
@login_required(login_url='login')
@require_POST
def react_to_message(request, pk):
    msg   = get_object_or_404(DailyMessage, pk=pk)
    data  = json.loads(request.body)
    emoji = data.get('emoji')

    valid_emojis = ['❤️', '🙏', '✨', '😢', '🔥']
    if emoji not in valid_emojis:
        return JsonResponse({'error': 'Invalid emoji'}, status=400)

    from .models import MessageReaction

    existing = MessageReaction.objects.filter(
        daily_message=msg, user=request.user
    ).first()

    if existing:
        if existing.emoji == emoji:
            existing.delete()
            user_reaction = None
        else:
            existing.emoji = emoji
            existing.save()
            user_reaction = emoji
    else:
        MessageReaction.objects.create(
            daily_message=msg, user=request.user, emoji=emoji
        )
        user_reaction = emoji

    reaction_counts = {
        e: msg.reactions.filter(emoji=e).count()
        for e in valid_emojis
    }

    return JsonResponse({
        'user_reaction':   user_reaction,
        'reaction_counts': reaction_counts,
        'total_reactions': msg.reactions.count(),
    })


@login_required(login_url='login')
@require_POST
def share_message(request, pk):
    msg = get_object_or_404(DailyMessage, pk=pk)
    # Import here to avoid circular import at module level
    from .models import DailyMessageShare

    share, created = DailyMessageShare.objects.get_or_create(
        daily_message=msg,
        user=request.user,
    )
    share_count = msg.shares.count()
    return JsonResponse({'share_count': share_count, 'created': created})