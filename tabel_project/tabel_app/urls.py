from rest_framework import routers
from django.urls import path, include
from .views import (AdminListAPIView, AdminDetailAPIView,
                    MentorProfileViewSet, StudentProfileViewSet,
                    GroupListAPIView, GroupDetailAPIView)


router = routers.SimpleRouter()
router.register(r'mentor', MentorProfileViewSet)
router.register(r'student', StudentProfileViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('user/', AdminListAPIView.as_view(), name='user-list'),
    path('user/<int:pk>/', AdminDetailAPIView.as_view(), name='user-detail'),
    path('group/', GroupListAPIView.as_view(), name='group_list'),
    path('group/<int:pk>/', GroupDetailAPIView.as_view(), name='group_detail'),
]