import sys
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, JsonResponse
from django.http.response import HttpResponse
import datetime
from django.db.models import Sum, Count, Q, F, Case, When, Value, CharField

from .models import Answer, Question, Quiz, Take, UserAnswer
from accounts.models import Profile


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
    questions = Question.objects.filter(quiz=quiz, is_active=True).values('id', 'type').order_by('id')
    
    # get all answerd questions of this quiz.
    answered_questions = UserAnswer.objects.filter(user=request.user).values('question_id')
    
    # filter questions that are not answered yet.
    questions = questions.exclude(id__in=answered_questions)
    
    # get the first question.
    first_question = Question.objects.filter(id=1).first()
    # get the choices of the first question.
    choices = Answer.objects.filter(question=first_question).all()
    
    first_question_answers = {
        'instruction': first_question.instruction,
        'text_question': first_question.text_question,
        'choices': [
            {
                'image': choice.image_choice.url if choice.image_choice else None,
                'is_correct': choice.is_correct
            } for choice in choices
        ]
    }
    
    context = {
        'quiz': quiz,
        'questions': list(questions),
        'first_question': first_question_answers
    }
    
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
            
            # 
            # convert answer_time from miliseconds to TimeField.
            #
            # get the current date and time.
            date_time = datetime.datetime.now()
            # set the time part to 0.
            date_time = date_time.replace(hour=0, minute=0, second=0, microsecond=0)

            answer_time = (date_time + datetime.timedelta(milliseconds=int(answer_time))).time()
            
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
    
    # get the total number of correct answers.
    total_correct_answers = UserAnswer.objects.filter(
        user=request.user,
        question__quiz=quiz,
        answer__is_correct=True
    ).count()
    
    # get the total number of incorrect answers.
    total_incorrect_answers = UserAnswer.objects.filter(
        user=request.user,
        question__quiz=quiz,
        answer__is_correct=False
    ).count()
    
    # get the total time spent on the quiz.
    quiz_time = UserAnswer.objects.filter(
        user=request.user,
        question__quiz=quiz
    ).aggregate(
        Sum('answer_time')
    )['answer_time__sum']
    
    
    context = {
        'correct_answers': total_correct_answers,
        'incorrect_answers': total_incorrect_answers,
        'quiz_time': quiz_time,
    }

    return render(request, 'quiz/results.html', context)

@login_required
def dashboard(request):
    # get all 
    users_answers = UserAnswer.objects.order_by(
        'user'
    ).values(
        'user'
    ).annotate(
        user_id=F('user__id'),
        user_first_name=F('user__first_name'),
        user_last_name=F('user__last_name'),
        total_answers=Count('id'),
        total_correct_answers=Count('id', filter=Q(answer__is_correct=True)),
        total_incorrect_answers=Count('id', filter=Q(answer__is_correct=False)),
        total_time=Sum('answer_time')
    ).all()
    
    return render(request, 'quiz/dashboard.html', {'users_answers': users_answers})

@login_required
@csrf_exempt
def user_detailed_results(request):
    if request.method == 'POST':
        try:
            # get the user id from the request.
            user_id = int(request.POST['user_id'])
            
            # get the user's information.
            user = Profile.objects.filter(
                user__id=user_id
            ).annotate(
                first_name = F('user__first_name'),
                last_name = F('user__last_name')
            ).values(
                'first_name', 'last_name', 'sex', 'birth_date',
                'academic_degree', 'aphasia_type', 'injury_date', 
                'address', 'phone_number'
            )
                        
            # get the user's answers.
            user_answers = UserAnswer.objects.filter(
                user__id=user_id
            ).annotate(
                qn_type=F('question__type'),
                qn_id=F('question__id'),
                qn_label=F('question__label'),
                # get the answer if it's correct using when and case.
                user_answer = Case(
                    When(answer__is_correct=True, then=Value('+')),
                    default=F('answer__label'),
                    output_field=CharField()
                )
            ).values(
                'qn_type', 'qn_id', 'qn_label', 'user_answer', 'answer_time'
            ).order_by('qn_id')
            
            user_answers = list(user_answers)
            # loop through the user's answers and add the question's correct answer to the user's answers.
            for i in range(len(user_answers)):
                correct_answer_label = Answer.objects.filter(
                    question=user_answers[i]['qn_id'],
                    is_correct=True
                ).values_list('label', flat=True).first()
                user_answers[i]['correct_answer'] = correct_answer_label
            
            # construct the response.
            response = {
                'user': user[0],
                'answers': user_answers
            }
            
        except:
            e = sys.exc_info()
            return HttpResponse(e)
        return JsonResponse(response, safe=False)
    else:
        raise Http404
            

@login_required
@csrf_exempt
def delete_user_answers(request):
    if request.method == 'POST':
        try:
            # get the user id from the request.
            user_id = int(request.POST['user_id'])
            
            # delete the user's answers.
            UserAnswer.objects.filter(
                user__id=user_id
            ).delete()
            
            # construct the response.
            response = {
                'status': 'success'
            }
            
        except:
            e = sys.exc_info()
            return HttpResponse(e)
        return JsonResponse(response, safe=False)
    else:
        raise Http404
            
