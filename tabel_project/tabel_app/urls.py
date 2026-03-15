from rest_framework import routers
from django.urls import path, include
from .views import (CustomLoginView, LogoutView, MentorProfileViewSet,
                    StudentProfileViewSet, LessonViewSet,
                    LessonRecordCreateAPIView, LessonRecordEditAPIView,
                    GroupListAPIView, GroupDetailAPIView,
                    MonthlyReportListAPIView, MoveStudentAPIView)

router = routers.SimpleRouter()
router.register(r'mentor', MentorProfileViewSet)
router.register(r'student', StudentProfileViewSet)
router.register(r'lesson', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', CustomLoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('lesson-record/', LessonRecordCreateAPIView.as_view(), name='create_lesson_record'),
    path('lesson-record/<int:pk>/', LessonRecordEditAPIView.as_view(), name='edit_lesson_record'),
    path('group/', GroupListAPIView.as_view(), name='group_list'),
    path('group/<int:pk>/', GroupDetailAPIView.as_view(), name='group_detail'),
    path('monthly-report/', MonthlyReportListAPIView.as_view(), name='monthly_report'),
    path('admin/move-student/', MoveStudentAPIView.as_view(), name='move_student')]
