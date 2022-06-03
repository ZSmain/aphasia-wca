from django.db import models

# extend the User model.
from django.contrib.auth.models import User

# create a profile model.
class Profile(models.Model):
    SEX_CHOICES = [
        ('male', 'ذكر'),
        ('female', 'أنثى')
    ]
    ACADEMIC_DEGREE_CHOICES = [
        ('elementry-school', 'إبتدائي'),
        ('middle-school', 'متوسط'),
        ('high-shool', 'ثانوي'),
        ('baccalaureate', 'بكلوريا'),
        ('licence', 'ليسانس'),
        ('master', 'ماستر'),
        ('doctorate', 'دكتوراه')
    ]
    APHASIA_TYPE_CHOICES = [
        ('healthy', 'غير مصاب'),
        ('wernicke', 'حسية'),
        ('broca', 'حركية'),
        ('mixte', 'مختلطة'),
        ('conduction', 'توصيلية'),
        ('conduction', 'نسيانية'),
        ('global', 'كلية')
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # add a field for the user's sex.
    sex = models.CharField(max_length=10, choices=SEX_CHOICES, default='male')
    # add a field for the user's birthdate.
    birth_date = models.DateField(blank=True, null=True)
    # address field
    address =  models.CharField(max_length=250, blank=True, null=True)
    # add a field for the user's academic level.
    academic_degree = models.CharField(max_length=35, choices=ACADEMIC_DEGREE_CHOICES, blank=True, null=True)
    # type of aphasia field
    aphasia_type = models.CharField(max_length=35, choices=APHASIA_TYPE_CHOICES, blank=True, null=True)
    # phone number field
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    # injury date field
    injury_date = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'

    