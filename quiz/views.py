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
    questions = Question.objects.filter(quiz=quiz).values('id', 'type').order_by('id')
    
    context = {'quiz': quiz, 'questions': list(questions)}
    
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

@login_required
def results(request, quiz_id):
    quiz = Quiz.objects.filter(id=quiz_id).first()
    
    # get all questions ids of this quiz.
    questions_ids = Question.objects.filter(quiz=quiz).values_list('id', flat=True)
    
    # get all user's answers.
    user_answers = UserAnswer.objects.filter(user=request.user, question_id__in=questions_ids).all()
    
    # get all questions.
    questions = Question.objects.filter(id__in=questions_ids).all()
    
    # get all choices.
    choices = Answer.objects.filter(question_id__in=questions_ids).all()
    
    # get all correct answers.
    correct_answers = Answer.objects.filter(question_id__in=questions_ids, is_correct=True).all()
    
    # get all user's answers.
    user_answers_ids = user_answers.values_list('answer_id', flat=True)
    
    # get all correct answers ids.
    correct_answers_ids = correct_answers.values_list('id', flat=True)
    
    # get all user's answers that are correct.
    correct_answers_ids_set = set(correct_answers_ids)
    user_answers_ids_set = set(user_answers_ids)
    correct_answers_ids_set_intersection = correct_answers_ids_set.intersection(user_answers_ids_set)
    
    # get all user's answers that are incorrect.
    incorrect_answers_ids_set = correct_answers_ids_set_intersection.difference(user_answers_ids_set)
    
    # get all correct answers that are incorrect.
    incorrect_answers_ids = list(incorrect_answers_ids_set)
    
    # get all user's answers that are incorrect.
    incorrect_answers_ids_set = correct_answers_ids_set_intersection.difference(user_answers_ids_set)
    
    context = {
        'quiz': quiz,
        'questions': questions,
        'choices': choices,
        'user_answers': user_answers,
        'correct_answers': correct_answers,
        'incorrect_answers': Answer.objects.filter(id__in=incorrect_answers_ids).all(),
        'user_answers_ids': user_answers_ids,
        'correct_answers_ids': correct_answers_ids,
        'incorrect_answers_ids': incorrect_answers_ids,
        'correct_answers_ids_set': correct_answers_ids_set,
        'user_answers_ids_set': user_answers_ids_set,
        'correct_answers_ids_set_intersection': correct_answers_ids_set_intersection,
        'incorrect_answers_ids_set': incorrect_answers_ids_set,
    }

    return render(request, 'quiz/results.html', context)