from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=100)
    UserRole = (
    ('MENTOR', 'MENTOR'),
    ('STUDENT', 'STUDENT'))
    role = models.CharField(max_length=32, choices=UserRole)


class MentorProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)


class Group(models.Model):
    course_name = models.CharField(max_length=100)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    study_days = models.DateField()


class StudentProfile(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = PhoneNumberField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.data

class LessonRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2)
