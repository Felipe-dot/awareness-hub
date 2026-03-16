import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'awareness_hub.settings')
django.setup()

from journal.models import User, MoodTag, JournalEntry, TherapySession

def seed():
    print("Seeding data...")
    
    tags_to_create = ["Anxious", "Insight", "Confluence", "Awareness", "Joyful", "Tired", "Connected"]
    mood_tags = []
    for tag_name in tags_to_create:
        tag, created = MoodTag.objects.get_or_create(name=tag_name)
        mood_tags.append(tag)
        if created:
            print(f"Created tag: {tag_name}")

    user, created = User.objects.get_or_create(username="tester")
    if created:
        user.set_password("testpass123")
        user.save()
        print("Created user: tester (pass: testpass123)")

    if not JournalEntry.objects.filter(user=user).exists():
        now = timezone.now()
        contents = [
            "Feeling a bit overwhelmed with work today.",
            "Had a great breakthrough in therapy.",
            "Noticed I tend to withdraw when I'm stressed.",
            "Feeling very in tune with my emotions.",
            "A quiet day of reflection.",
            "Practicing awareness of my surroundings.",
            "Insight into my confluence patterns."
        ]
        
        for i in range(14):
            entry_date = now - timedelta(days=14-i)
            entry = JournalEntry.objects.create(
                user=user,
                content=random.choice(contents),
                mood_score=random.randint(3, 9),
            )
            JournalEntry.objects.filter(id=entry.id).update(created_at=entry_date)
            
            entry.tags.add(*random.sample(mood_tags, random.randint(1, 3)))
            
        print("Created 14 sample journal entries.")

    if not TherapySession.objects.filter(user=user).exists():
        TherapySession.objects.create(
            user=user,
            date=timezone.now().date() - timedelta(days=2),
            main_insights="Focused on the boundary between self and environment.",
            next_steps="Practice sensory awareness exercises twice a day."
        )
        print("Created sample therapy session.")

    print("Seeding complete! You can now log in as 'tester' with 'testpass123' to see the chart and test tags.")

if __name__ == "__main__":
    seed()
