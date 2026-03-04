from django.contrib import admin
from .models import UserProfile, MentorProfile, StudentProfile, Group, Lesson, LessonRecord


admin.site.register(UserProfile)
admin.site.register(MentorProfile)
admin.site.register(StudentProfile)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(LessonRecord)

