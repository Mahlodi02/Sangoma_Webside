from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Booking(models.Model):
    name = models.CharField(max_length=100)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.service.name}"
    

class Review(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class DailyMessage(models.Model):
    text = models.TextField(help_text="Write the daily encouragement shown on the homepage.")
    active = models.BooleanField(default=True, help_text="Only active messages are shown on the homepage.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Daily message ({self.created_at:%Y-%m-%d %H:%M})"


class DailyMessageComment(models.Model):
    daily_message = models.ForeignKey(
        DailyMessage,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(help_text="Share how this message encouraged you.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.user.username if self.user else 'Anonymous'} on {self.daily_message}"
