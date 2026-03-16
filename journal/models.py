from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    pass

class MoodTag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class JournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journal_entries')
    content = models.TextField()
    mood_score = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    tags = models.ManyToManyField(MoodTag, related_name='entries', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Entry by {self.user.username} on {self.created_at.strftime('%Y-%m-%d')}"

class TherapySession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='therapy_sessions')
    date = models.DateField()
    main_insights = models.TextField()
    next_steps = models.TextField()

    def __str__(self):
        return f"Session for {self.user.username} on {self.date}"
