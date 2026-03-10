from django.contrib import admin
from .models import MentorProfile, StudentProfile, Group, Lesson, LessonRecord, MonthlyReport


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'end_date')
    fields = ('course_name', 'mentor', 'study_days', 'duration_months', 'created_at', 'end_date')


admin.site.register(MentorProfile)
admin.site.register(StudentProfile)
admin.site.register(Lesson)
admin.site.register(LessonRecord)
admin.site.register(MonthlyReport)