from multiprocessing import context
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Answer, Question, Quiz, Take, UserAnswer


@login_required
def home(request):
    # get all quizes.
    quizes = Quiz.objects.all()
    
    context = {'quizes': quizes}
    
    return render(request, 'quiz/home.html', context)

@login_required
def dashboard(request):
    return render(request, 'quiz/dashboard.html')

@login_required
def quiz(request, quiz_id):
    
    quiz = Quiz.objects.filter(id=quiz_id).first()
    
    # get all questions ids of this quiz.
    questions_ids = Question.objects.filter(quiz=quiz).values_list('id', flat=True)
    
    context = {'quiz': quiz, 'questions_ids': questions_ids}
    
    return render(request, 'quiz/quiz.html', context)

