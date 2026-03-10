from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from dateutil.relativedelta import relativedelta


class MentorProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Group(models.Model):
    course_name = models.CharField(max_length=100)
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    StudyDaysChoices = (
        ('Пн Ср Сб', 'Пн Ср Сб'),
        ('Вт Чт Вс', 'Вт Чт Вс'))
    study_days = models.CharField(max_length=32, choices=StudyDaysChoices)
    created_at = models.DateField(auto_now_add=True)
    duration_months = models.IntegerField(default=1)
    end_date = models.DateField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new or self.duration_months:
            self.end_date = self.created_at + relativedelta(months=self.duration_months)
            Group.objects.filter(pk=self.pk).update(end_date=self.end_date)

    def __str__(self):
        return self.course_name


class StudentProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    parent_name = models.CharField(max_length=100)
    parent_phone = PhoneNumberField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()


class Lesson(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='lesson_group')
    data = models.DateField()

    def __str__(self):
        return str(self.data)


class LessonRecord(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_list')
    grade = models.CharField(max_length=3)


class MonthlyReport(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    month = models.DateField()
    total_grade = models.IntegerField(default=0)
    visit_count = models.IntegerField(default=0)
    average_grade = models.FloatField(default=0.0)

    class Meta:
        unique_together = ('student', 'group', 'month')

    def __str__(self):
        return f"{self.student} - {self.month}"