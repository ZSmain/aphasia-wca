from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.dashboard, name='dashboard'),
    path('quiz/<int:quiz_id>/', views.quiz, name='quiz'),
    path('question_choices.json', views.get_question_choices, name='get_question_choices'),
    # add the path for the results page
    path('quiz/results/<int:quiz_id>/', views.results, name='results'),
    # path to the user detailed results view.
    path('detailed_results.json', views.user_detailed_results, name='user_detailed_results'),
    # path to the user answers deletion view.
    path('delete_answers.json', views.delete_user_answers, name='delete_user_answers'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)