from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register_view, name='register'),
    path('journal', views.journal, name='journal'),
    path('sessions', views.therapy_sessions, name='sessions'),
    
    path('api/mood-trend/', views.mood_trend_data, name='mood_trend_data'),
    path('api/save-draft/', views.save_draft, name='save_draft'),
    path('api/toggle-tag/', views.toggle_tag, name='toggle_tag'),
    path('api/create-tag/', views.create_tag, name='create_tag'),
]
