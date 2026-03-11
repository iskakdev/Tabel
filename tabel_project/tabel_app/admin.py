from django.contrib import admin
from .models import Admin, MentorProfile, StudentProfile, Group, Lesson, LessonRecord

admin.site.register(Admin)
admin.site.register(MentorProfile)
admin.site.register(StudentProfile)
admin.site.register(Group)
admin.site.register(Lesson)
admin.site.register(LessonRecord)

