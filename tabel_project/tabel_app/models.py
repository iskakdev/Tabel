from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Admin(models.Model):
    full_name = models.CharField(max_length=100)
    UserRole = (
    ('MENTOR', 'MENTOR'),
    ('STUDENT', 'STUDENT'))
    role = models.CharField(max_length=32, choices=UserRole)


class MentorProfile(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)



class Group(models.Model):
    course_name = models.CharField(max_length=100)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    StudyDaysChoices = (
    ('Пн Ср Сб', 'Пн Ср Сб'),
    ('Вт Чт Вс', 'Вт Чт Вс'))
    study_days = models.CharField(max_length=32, choices=StudyDaysChoices)

    def __str__(self):
        return self.course_name


class StudentProfile(models.Model):
    user = models.ForeignKey(Admin, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = PhoneNumberField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.parent_name


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_group')
    data = models.DateField(auto_now=True)

    def __str__(self):
        return self.data


class LessonRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_list')
    grade = models.CharField(max_length=2)
