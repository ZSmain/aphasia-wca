from django.db import models

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    header_image = models.ImageField(upload_to='quiz/images/', blank=True)

    def __str__(self):
        return self.title
    
class Question(models.Model):
    TYPE_CHOICES = (
        'single', 'multiple', 'text',
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question = models.ImageField(upload_to='quiz/images/')
    type = models.CharField(max_length=200)
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.text

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    
    image_choice = models.ImageField(upload_to='quiz_images', blank=True, null=True)
    text_choice = models.TextField(blank=True, null=True)
    label = models.CharField(max_length=200, blank=True, null=True)
    
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.question.label} - {self.label}'

class Take(models.Model):
    STATUS_CHOICES = (
        ('started', 'Started'),
        ('paused', 'Paused'),
        ('finished', 'Finished'),
        ('failed', 'Failed'),
    )
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='started')
    
    started_time = models.DateTimeField(null=True)
    finished_time = models.DateTimeField(null=True)
    
class UserAnswer(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    
    answer_time = models.TimeField(null=True)

    def __str__(self):
        return self.user.username