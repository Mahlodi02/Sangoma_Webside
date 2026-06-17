from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User


class Service(models.Model):
    name        = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    name       = models.CharField(max_length=100)
    service    = models.ForeignKey(Service, on_delete=models.CASCADE)
    date       = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service.name}"


class Review(models.Model):
    name       = models.CharField(max_length=100)
    message    = models.TextField()
    rating     = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DailyMessage(models.Model):
    text       = models.TextField(
        help_text="Type today's encouragement message here."
    )
    active     = models.BooleanField(
        default=True,
        help_text="Tick this to show the message. Untick to hide it."
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message — {self.created_at:%d %b %Y}"

    def total_reactions(self):
        return self.reactions.count()

    def reaction_count(self, emoji):
        return self.reactions.filter(emoji=emoji).count()


class DailyMessageComment(models.Model):
    daily_message = models.ForeignKey(
        DailyMessage, on_delete=models.CASCADE, related_name='comments'
    )
    user       = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Anonymous'}"
 
class DailyMessageShare(models.Model):
    daily_message = models.ForeignKey(
        DailyMessage, on_delete=models.CASCADE, related_name='shares'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('daily_message', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username if self.user else 'Anonymous'} shared {self.daily_message}"

class MessageReaction(models.Model):
    EMOJI_CHOICES = [
        ('❤️',  'Love'),
        ('🙏',  'Grateful'),
        ('✨',  'Inspired'),
        ('😢',  'Touched'),
        ('🔥',  'Powerful'),
    ]
    daily_message = models.ForeignKey(
        DailyMessage, on_delete=models.CASCADE, related_name='reactions'
    )
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    emoji = models.CharField(max_length=10, choices=EMOJI_CHOICES)

    class Meta:
        unique_together = ('daily_message', 'user')

    def __str__(self):
        return f"{self.user.username} reacted {self.emoji}"