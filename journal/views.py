from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from .models import User, JournalEntry, TherapySession, MoodTag
import json

def login_view(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username", "")
        password = data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "journal/login.html", {"message": "Invalid credentials."})
    return render(request, "journal/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

def register_view(request):
    if request.method == "POST":
        data = request.POST
        username = data.get("username", "")
        email = data.get("email", "")
        password = data.get("password", "")
        confirmation = data.get("confirmation", "")

        if password != confirmation:
            return render(request, "journal/register.html", {"message": "Passwords must match."})

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return redirect("index")
        except IntegrityError:
            return render(request, "journal/register.html", {"message": "Username already taken."})
    return render(request, "journal/register.html")

@login_required
def index(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    entries = JournalEntry.objects.filter(user=request.user, created_at__date__gte=thirty_days_ago)

    most_frequent_tag = None
    if entries.exists():
        tag_counts = {}
        for entry in entries:
            for tag in entry.tags.all():
                weekday = entry.created_at.strftime('%A')
                key = (weekday, tag.name)
                tag_counts[key] = tag_counts.get(key, 0) + 1
        
        if tag_counts:
            best_pattern = max(tag_counts, key=tag_counts.get)
            most_frequent_tag = {
                'weekday': best_pattern[0],
                'tag': best_pattern[1],
                'count': tag_counts[best_pattern]
            }

    return render(request, "journal/index.html", {
        "insight": most_frequent_tag
    })

@login_required
def journal(request):
    tags = MoodTag.objects.all()
    today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
    draft = JournalEntry.objects.filter(user=request.user, created_at__gte=today_start).first()
    
    return render(request, "journal/journal_entry.html", {
        "tags": tags,
        "draft": draft
    })

@login_required
def save_draft(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            content = data.get("content", "")
            mood_score = int(data.get("mood_score", 5))
            
            today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
            draft, created = JournalEntry.objects.get_or_create(
                user=request.user, 
                created_at__gte=today_start,
                defaults={'content': content, 'mood_score': mood_score}
            )
            
            if not created:
                draft.content = content
                draft.mood_score = mood_score
                draft.save()
                
            return JsonResponse({"status": "success", "id": draft.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)

@login_required
def toggle_tag(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            entry_id = data.get("entry_id")
            tag_id = data.get("tag_id")
            action = data.get("action")
            
            entry = JournalEntry.objects.get(id=entry_id, user=request.user)
            tag = MoodTag.objects.get(id=tag_id)
            
            if action == 'add':
                entry.tags.add(tag)
            elif action == 'remove':
                entry.tags.remove(tag)
                
            return JsonResponse({"status": "success", "tag": tag.name, "action": action})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)

@login_required
def create_tag(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            tag_name = data.get("name", "").strip()
            entry_id = data.get("entry_id")
            
            if not tag_name:
                return JsonResponse({"status": "error", "message": "Tag name cannot be empty"}, status=400)
            
            tag, created = MoodTag.objects.get_or_create(name=tag_name)
            
            if entry_id:
                entry = JournalEntry.objects.get(id=entry_id, user=request.user)
                entry.tags.add(tag)
                
            return JsonResponse({
                "status": "success", 
                "tag_id": tag.id, 
                "tag_name": tag.name,
                "created": created
            })
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=400)
    return JsonResponse({"status": "error"}, status=400)

@login_required
def therapy_sessions(request):
    sessions = TherapySession.objects.filter(user=request.user).order_by('-date')
    recent_entries = JournalEntry.objects.filter(
        user=request.user, 
        created_at__gte=timezone.now() - timedelta(days=30)
    ).order_by('-created_at')
    
    return render(request, "journal/therapy_sessions.html", {
        "sessions": sessions,
        "recent_entries": recent_entries
    })

@login_required
def mood_trend_data(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)
    entries = JournalEntry.objects.filter(
        user=request.user,
        created_at__date__gte=thirty_days_ago
    ).order_by('created_at')

    labels = []
    data = []
    for entry in entries:
        labels.append(entry.created_at.strftime('%Y-%m-%d'))
        data.append(entry.mood_score)

    return JsonResponse({'labels': labels, 'data': data})

@login_required
def word_cloud_data(request):
    STOPWORDS = {
        'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you',
        'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his',
        'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
        'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
        'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
        'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having',
        'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if',
        'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for',
        'with', 'about', 'against', 'between', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down',
        'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further',
        'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
        'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
        'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
        'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
        'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', 'couldn',
        'didn', 'doesn', 'hadn', 'hasn', 'haven', 'isn', 'ma', 'mightn',
        'mustn', 'needn', 'shan', 'shouldn', 'wasn', 'weren', 'won', 'wouldn',
        'feel', 'felt', 'feeling', 'think', 'thinking', 'thought', 'today',
        'day', 'time', 'like', 'really', 'much', 'also', 'still', 'even',
        'get', 'got', 'know', 'want', 'need', 'lot', 'things', 'something',
        'everything', 'nothing', 'anything', 'one', 'two', 'would', 'could',
    }

    import re
    from collections import Counter

    thirty_days_ago = timezone.now() - timedelta(days=30)
    entries = JournalEntry.objects.filter(
        user=request.user,
        created_at__date__gte=thirty_days_ago
    )

    word_counts = Counter()
    for entry in entries:
        if entry.content:
            words = re.findall(r"[a-z']+", entry.content.lower())
            for word in words:
                clean = word.strip("'")
                if clean and len(clean) > 2 and clean not in STOPWORDS:
                    word_counts[clean] += 1

    top5 = [{'word': w, 'count': c} for w, c in word_counts.most_common(5)]
    return JsonResponse({'words': top5})
