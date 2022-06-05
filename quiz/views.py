from multiprocessing import context
import sys
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.http.response import HttpResponse
import datetime

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

@login_required
@csrf_exempt
def get_question_choices(request):
    if request.method == 'POST':
        try:
            quiz_id = int(request.POST['quiz_id'])
            question_id = int(request.POST['question_id'])
            choice_id = request.POST['choice_id']
            answer_time = request.POST['answer_time']
            next_question_id = request.POST['next_question_id']
            
            # convert answer_time from miliseconds to TimeField.
            answer_time = datetime.datetime.fromtimestamp(int(answer_time))
            
            response = {'status': 'failed'}
            
            # check if the choice_id is 'null' (first question).
            if choice_id == 'null':
                # get the quiz object.
                quiz = Quiz.objects.filter(id=quiz_id).first()
                
                # if the user didn't take this quiz, create a new Take object.
                take = Take.objects.filter(user=request.user, quiz=quiz).first()
                if not take:
                    Take(
                        user=request.user,
                        quiz=quiz,
                        status='started',
                        started_time=datetime.datetime.now()
                    ).save()
            
                # get the question.
                question = Question.objects.filter(id=question_id).first()
                
                # get the question's choices.
                choices = Answer.objects.filter(question=question_id).all()
            
            # reached the last question.
            elif next_question_id == 'undefined':
                response = {'status': 'finished'}
            
            # save the user's answer and get the next question.
            else:
                choice_id = int(choice_id)
                next_question_id = int(next_question_id)
                
                # save the user's answer.
                UserAnswer(
                    user=request.user,
                    question_id=question_id,
                    answer_id=choice_id,
                    answer_time=answer_time
                ).save()
                
                # get the next question.
                question = Question.objects.filter(id=next_question_id).first()
                
                # get the next question's choices.
                choices = Answer.objects.filter(question=question).all()
            
            # create json response with question and choices if nex_question_id is not 'undefined'.
            if next_question_id != 'undefined':
                response = {
                    'status': 'success',
                    'question': [
                        {
                            'instruction': question.instruction,
                            'text': question.text_question,
                            'image': question.image_question.url if question.image_question else None,
                            'paragraph': question.paragraph,
                            'type': question.type,
                        }
                    ],
                    'choices': [
                        {
                            'id': choice.id,
                            'text': choice.text_choice,
                            'image': choice.image_choice.url if choice.image_choice else None
                        } for choice in choices
                    ]
                }

        except:
            e = sys.exc_info()
            return HttpResponse(e)
        return JsonResponse(response, safe=False)
    else:
        raise Http404

