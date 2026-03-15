from rest_framework.permissions import BasePermission


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'studentprofile')


class IsMentor(BasePermission):
    def has_permission(self, request, view):
        return hasattr(request.user, 'mentorprofile')


class IsMentorOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_staff or hasattr(request.user, 'mentorprofile')