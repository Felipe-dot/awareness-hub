from django.contrib import admin
from .models import User, MoodTag, JournalEntry, TherapySession

admin.site.register(User)
admin.site.register(MoodTag)
admin.site.register(JournalEntry)
admin.site.register(TherapySession)
