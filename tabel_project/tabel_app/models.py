from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=100)
    UserRole = (
    ('ADMIN', 'ADMIN'),
    ('MENTOR', 'MENTOR'),
    ('STUDENT', 'STUDENT'))


class MentorProfile(UserProfile):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    SubjectChoices = (
    ('Python', 'Python'),
    ('AI', 'AI'),
    ('FullStack', 'FullStack'),
    ('Frontend', 'Frontend'))


class StudentProfile(UserProfile):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = PhoneNumberField()


class Group(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.DateField()
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    study_days = models.DateField()