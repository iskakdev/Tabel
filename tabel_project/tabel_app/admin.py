from django.contrib import admin
from .models import MentorProfile, StudentProfile, Group, Lesson, LessonRecord, MonthlyReport


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at', 'end_date')
    fields = ('course_name', 'mentor', 'study_days', 'duration_months', 'created_at', 'end_date')
    list_display = ('course_name', 'mentor', 'study_days', 'created_at', 'end_date')
    search_fields = ('course_name',)


@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'user')
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'group', 'parent_name', 'parent_phone')
    list_filter = ('group',)
    search_fields = ('user__first_name', 'user__last_name')


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('date', 'group')
    list_filter = ('group',)
    ordering = ('-date',)


@admin.register(LessonRecord)
class LessonRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'lesson', 'grade', 'attendance', 'late_minutes')
    list_filter = ('attendance',)
    search_fields = ('student__user__first_name', 'student__user__last_name')


@admin.register(MonthlyReport)
class MonthlyReportAdmin(admin.ModelAdmin):
    list_display = ('student', 'group', 'month', 'average_grade', 'visit_count')
    list_filter = ('group',)
    ordering = ('-month',)
