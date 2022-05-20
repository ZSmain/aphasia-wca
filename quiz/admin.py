import imp
from django.contrib import admin

from .models import Quiz, Question, Answer

# Register your models here.

# Register the Quiz model.
admin.site.register(Quiz)

# Register the Question model.
admin.site.register(Question)

# Register the Answer model.
admin.site.register(Answer)

