from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Quiz


@login_required
def home(request):
    quizes = Quiz.objects.all()
    
    context = {'quizes': quizes}
    
    return render(request, 'quiz/home.html', context)

@login_required
def dashboard(request):
    return render(request, 'quiz/dashboard.html')

