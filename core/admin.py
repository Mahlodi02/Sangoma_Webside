from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Service, Booking, Review, DailyMessage, DailyMessageComment, MessageReaction


# ── USER ───────────────────────────────────────────────────────
class CustomUserAdmin(BaseUserAdmin):
    list_display  = ['username', 'email', 'first_name', 'last_name', 'date_joined', 'is_active']
    list_filter   = ['is_active', 'is_staff']
    search_fields = ['username', 'email']
    ordering      = ['-date_joined']

try:
    admin.site.unregister(User)
except Exception:
    pass

admin.site.register(User, CustomUserAdmin)


# ── SERVICE ────────────────────────────────────────────────────
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display  = ['name', 'description']
    search_fields = ['name']


# ── BOOKING ────────────────────────────────────────────────────
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['name', 'service', 'date', 'created_at']
    list_filter   = ['service', 'date']
    search_fields = ['name']
    ordering      = ['-created_at']


# ── REVIEW ─────────────────────────────────────────────────────
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['name', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['name', 'message']
    ordering      = ['-created_at']


# ── REACTION INLINE ────────────────────────────────────────────
class MessageReactionInline(admin.TabularInline):
    model           = MessageReaction
    extra           = 0
    readonly_fields = ['user', 'emoji']
    can_delete      = True


# ── DAILY MESSAGE COMMENT INLINE ───────────────────────────────
class DailyMessageCommentInline(admin.TabularInline):
    model           = DailyMessageComment
    extra           = 0
    readonly_fields = ['user', 'text', 'created_at']
    can_delete      = False


# ── DAILY MESSAGE ───────────────────────────────────────────────
@admin.register(DailyMessage)
class DailyMessageAdmin(admin.ModelAdmin):
    list_display  = ['text', 'active', 'created_at']
    list_filter   = ['active', 'created_at']
    search_fields = ['text']
    ordering      = ['-created_at']
    inlines       = [DailyMessageCommentInline, MessageReactionInline]


# ── DAILY MESSAGE COMMENT ───────────────────────────────────────
@admin.register(DailyMessageComment)
class DailyMessageCommentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'daily_message', 'text', 'created_at']
    list_filter   = ['created_at']
    search_fields = ['user__username', 'text']
    ordering      = ['-created_at']


# ── MESSAGE REACTION ────────────────────────────────────────────
@admin.register(MessageReaction)
class MessageReactionAdmin(admin.ModelAdmin):
    list_display  = ['user', 'daily_message', 'emoji']
    list_filter   = ['emoji']
    search_fields = ['user__username']