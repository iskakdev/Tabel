from .models import Admin, MentorProfile, StudentProfile, Group, Lesson, LessonRecord
from .serializers import (AdminListSerializer,
                          AdminDetailSerializer, MentorProfileSerializer, StudentProfileSerializer,
                          LessonSerializer, LessonRecordSerializer, LoginSerializer,
                          GroupListSerializer, GroupDetailSerializer)
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class AdminDetailAPIView(generics.RetrieveAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminDetailSerializer


class AdminListAPIView(generics.ListAPIView):
    queryset = Admin.objects.all()
    serializer_class = AdminListSerializer

    def get_queryset(self):
        return Admin.objects.filter(id = self.request.user.id)


class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer

    def get_queryset(self):
        return Admin.objects.filter(id = self.request.user.id)

class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class =  StudentProfileSerializer

    def get_queryset(self):
        return Admin.objects.filter(id = self.request.user.id)

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRecordViewSet(viewsets.ModelViewSet):
    queryset = LessonRecord.objects.all()
    serializer_class = LessonRecordSerializer

class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer

class GroupDetailAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupDetailSerializer
