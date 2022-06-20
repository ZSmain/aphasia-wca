from django.contrib import admin

from .models import Quiz, Question, Answer

# Register your models here.

# Register the Quiz model.
admin.site.register(Quiz)

# Register the Question model.
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'type', 'instruction', 'image_question', 'text_question', 'paragraph', 'label')
    
    search_fields = ['type', 'label', 'text_question', 'paragraph']

# Register the Answer model.
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'image_choice', 'text_choice', 'label', 'is_correct')
    
    search_fields = ['question__label', 'label', 'text_choice']

