from django.urls import URLPattern, path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    # path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
]