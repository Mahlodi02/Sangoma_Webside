from django.contrib import admin
from .models import Service, Booking, Review, DailyMessage, DailyMessageComment


class DailyMessageCommentInline(admin.TabularInline):
    model = DailyMessageComment
    extra = 0
    readonly_fields = ('user', 'text', 'created_at')
    can_delete = False


class DailyMessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'active', 'created_at')
    list_filter = ('active', 'created_at')
    search_fields = ('text',)
    inlines = [DailyMessageCommentInline]


admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(DailyMessage, DailyMessageAdmin)
admin.site.register(DailyMessageComment)
