from .models import MentorProfile, StudentProfile, Group, Lesson, LessonRecord, MonthlyReport
from .serializers import (MentorProfileSerializer, StudentProfileSerializer,
                          LessonSerializer, LessonRecordSerializer, CreateLessonRecord,
                          LoginSerializer, GroupListSerializer,
                          MonthlyReportSerializer)
from rest_framework import viewsets, generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date


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


class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    serializer_class = StudentProfileSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class LessonRecordCreateAPIView(generics.CreateAPIView):
    queryset = LessonRecord.objects.all()
    serializer_class = CreateLessonRecord


class LessonRecordEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonRecord.objects.all()
    serializer_class = LessonRecordSerializer


class GroupListAPIView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupListSerializer


class GroupDetailAPIView(generics.RetrieveAPIView):
    queryset = Group.objects.all()

    def get(self, request, pk):
        group = Group.objects.get(pk=pk)
        all_time = request.query_params.get('all')
        month_param = request.query_params.get('month')

        lessons = Lesson.objects.filter(group=group)

        if all_time != 'true':
            if month_param:
                year, month = map(int, month_param.split('-'))
            else:
                today = date.today()
                year, month = today.year, today.month

            lessons = lessons.filter(data__year=year, data__month=month)

        records = LessonRecord.objects.filter(lesson__in=lessons)
        students = StudentProfile.objects.filter(group=group)

        students_data = []
        for student in students:
            student_records = records.filter(student=student)

            grades_by_date = {
                str(r.lesson.data): r.grade for r in student_records
            }

            total = 0
            count = 0
            for r in student_records:
                if r.grade == 'н':
                    continue
                grade_str = r.grade.replace('+', '').replace('-', '')
                if grade_str.isdigit():
                    total += int(grade_str)
                    count += 1

            average = round(total / count, 2) if count > 0 else 0

            students_data.append({
                "full_name": student.user.get_full_name(),
                "total_grade": total,
                "average_grade": average,
                "visit_count": count,
                "grades": grades_by_date,
            })

        return Response({
            "group": group.course_name,
            "start_date": str(group.created_at),
            "end_date": str(group.end_date),
            "lessons": [str(l.data) for l in lessons.order_by('data')],
            "students": students_data,
        })


class MonthlyReportListAPIView(generics.ListAPIView):
    queryset = MonthlyReport.objects.all()
    serializer_class = MonthlyReportSerializer