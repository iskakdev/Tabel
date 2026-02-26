from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    full_name = models.CharField(max_length=100)
    UserRole = (
    ('ADMIN', 'ADMIN'),
    ('MENTOR', 'MENTOR'),
    ('STUDENT', 'STUDENT'))
    role_user = models.CharField(max_length=10, choices=UserRole, default='ADMIN')

    def __str__(self):
        return f'{self.first_name}, {self.last_name} , {self.role_user}'

class MentorProfile(UserProfile):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    SubjectChoices = (
    ('Python', 'Python'),
    ('AI', 'AI'),
    ('FullStack', 'FullStack'),
    ('Frontend', 'Frontend'))
    role_mentor = models.CharField(max_length=10, choices=SubjectChoices, default='Python')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}, {self.role_mentor}'



class StudentProfile(UserProfile):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = PhoneNumberField()



class Group(models.Model):
    course_name = models.CharField(max_length=100)
    duration = models.DateField()
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    study_days = models.DateField()


class Lesson(models.Model):
    data = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.data


class LessonRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    grade = models.IntegerField(choices=[(i, str(i))for i in range(2,5)])
    Attendance = (
        ('Present', 'Present'),
        ('Absent', 'Absent')
    )
    attendance = models.CharField(max_length=77, choices=Attendance)


