import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tabel_project.settings')
django.setup()

from django.contrib.auth.models import User
from tabel_app.models import MentorProfile, StudentProfile, Group, Lesson, LessonRecord
from datetime import date
import random


# Users - менторы
mentor_names = [
    ('Алибек', 'Жаксыбеков'),
    ('Нурлан', 'Сейткали'),
]
mentor_users = []
for first, last in mentor_names:
    user, _ = User.objects.get_or_create(
        username=first.lower(),
        defaults={'first_name': first, 'last_name': last}
    )
    user.set_password('password123')
    user.save()
    mentor_users.append(user)

# Users - студенты
student_names = [
    ('Жаниш', 'Казыбаев'),
    ('Мираида', 'Эшпаева'),
    ('Эльвина', 'Надырбекова'),
    ('Аскат', 'Алтынбеков'),
    ('Ырысбек', 'Журабаев'),
    ('Лилия', 'Кубанычева'),
]
student_users = []
for first, last in student_names:
    user, _ = User.objects.get_or_create(
        username=first.lower(),
        defaults={'first_name': first, 'last_name': last}
    )
    user.set_password('password123')
    user.save()
    student_users.append(user)

# Mentor profiles
mentor_profiles = []
for user in mentor_users:
    profile, _ = MentorProfile.objects.get_or_create(user=user)
    mentor_profiles.append(profile)

# Groups
groups_data = [
    ('ИИ 1-группа', mentor_profiles[0], 'Пн Ср Сб', 6),
    ('Python 2-группа', mentor_profiles[1], 'Вт Чт Вс', 3),
]
groups = []
for course_name, mentor, study_days, duration in groups_data:
    group, _ = Group.objects.get_or_create(
        course_name=course_name,
        defaults={
            'mentor': mentor,
            'study_days': study_days,
            'duration_months': duration,
        }
    )
    groups.append(group)

# Student profiles
student_profiles = []
for i, user in enumerate(student_users):
    group = groups[0] if i < 4 else groups[1]
    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'parent_name': f'Родитель {user.first_name}',
            'parent_phone': f'+996700{str(i).zfill(6)}',
            'group': group,
        }
    )
    student_profiles.append(profile)

# Lessons — 6 уроков в текущем месяце
today = date.today()
lesson_dates = [
    date(today.year, today.month, d)
    for d in [3, 5, 8, 10, 12, 15]
]
lessons = []
for group in groups:
    for lesson_date in lesson_dates:
        lesson = Lesson.objects.filter(group=group, data=lesson_date).first()
        if not lesson:
            lesson = Lesson.objects.create(group=group, data=lesson_date)
        lessons.append(lesson)

# Lesson records
grades = ['5', '4', '5', '3', 'н', '+5', '-4', '5', '4', '5']
for lesson in lessons:
    group_students = [s for s in student_profiles if s.group == lesson.group]
    for student in group_students:
        if not LessonRecord.objects.filter(student=student, lesson=lesson).exists():
            LessonRecord.objects.create(
                student=student,
                lesson=lesson,
                grade=random.choice(grades)
            )

print('Данные успешно заполнены!')