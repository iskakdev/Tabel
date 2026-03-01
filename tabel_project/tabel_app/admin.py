from django.contrib import admin
from .models import UserProfile, MentorProfile, StudentProfile, Group, LessonDate, LessonList


admin.site.register(UserProfile)
admin.site.register(MentorProfile)
admin.site.register(StudentProfile)
admin.site.register(Group)
admin.site.register(LessonDate)
admin.site.register(LessonList)

