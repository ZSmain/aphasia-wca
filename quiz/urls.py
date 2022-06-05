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
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)