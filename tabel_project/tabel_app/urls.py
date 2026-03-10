from rest_framework import routers
from django.urls import path, include
from .views import (MentorProfileViewSet, StudentProfileViewSet,
                    LessonRecordCreateAPIView, LessonRecordEditAPIView,
                    GroupListAPIView, GroupDetailAPIView, MonthlyReportListAPIView)

router = routers.SimpleRouter()
router.register(r'mentor', MentorProfileViewSet)
router.register(r'student', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('create_lesson_record/', LessonRecordCreateAPIView.as_view(), name='create_lesson_record'),
    path('create_lesson_record/<int:pk>/', LessonRecordEditAPIView.as_view(), name='edit_lesson_record'),
    path('group/', GroupListAPIView.as_view(), name='group_list'),
    path('group/<int:pk>/', GroupDetailAPIView.as_view(), name='group_detail'),
    path('monthly_report/', MonthlyReportListAPIView.as_view(), name='monthly_report'),
]