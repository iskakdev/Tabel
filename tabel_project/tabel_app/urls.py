from rest_framework import routers
from django.urls import path, include
from .views import (UserProfileAPIViewSet, UserProfileDetailAPIView, UserProfileListAPIView,
                    MentorProfileViewSet, StudentProfileViewSet, GroupViewSet, LessonViewSet, LessonRecordViewSet)


router = routers.SimpleRouter()
router.register(r'user_register', UserProfileAPIViewSet)
router.register(r'mentor', MentorProfileViewSet)
router.register(r'student', StudentProfileViewSet)
router.register(r'group', GroupViewSet)
router.register(r'lesson', LessonViewSet)
router.register(r'lesson_record', LessonRecordViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', UserProfileListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user-detail')
]