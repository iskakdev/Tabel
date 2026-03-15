from .models import (MentorProfile, StudentProfile, Group, Lesson, LessonRecord, MonthlyReport)
from .serializers import (MentorProfileSerializer, StudentProfileSerializer, StudentProfileAdminSerializer,
                          LessonSerializer, LessonRecordSerializer, LoginSerializer, GroupListSerializer,
                          MonthlyReportSerializer)
from .permissions import IsMentorOrAdmin
from rest_framework import viewsets, generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from datetime import date
from collections import defaultdict


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({'detail': 'Неверные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            token = RefreshToken(request.data['refresh'])
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupQuerySetMixin:
    def get_group_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Group.objects.all()
        if hasattr(user, 'mentorprofile'):
            return Group.objects.filter(mentor=user.mentorprofile)
        if hasattr(user, 'studentprofile'):
            return Group.objects.filter(pk=user.studentprofile.group_id)
        return Group.objects.none()


class MentorProfileViewSet(viewsets.ModelViewSet):
    queryset = MentorProfile.objects.all()
    serializer_class = MentorProfileSerializer
    permission_classes = [IsAdminUser]


class StudentProfileViewSet(viewsets.ModelViewSet):
    queryset = StudentProfile.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return StudentProfileAdminSerializer
        return StudentProfileSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return StudentProfile.objects.select_related('user').all()
        if hasattr(user, 'studentprofile'):
            return StudentProfile.objects.filter(pk=user.studentprofile.pk)
        return StudentProfile.objects.none()


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRecordCreateAPIView(generics.CreateAPIView):
    queryset = LessonRecord.objects.all()
    serializer_class = LessonRecordSerializer
    permission_classes = [IsMentorOrAdmin]


class LessonRecordEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LessonRecord.objects.all()
    serializer_class = LessonRecordSerializer
    permission_classes = [IsMentorOrAdmin]


class GroupListAPIView(GroupQuerySetMixin, generics.ListAPIView):
    serializer_class = GroupListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_group_queryset()


class GroupDetailAPIView(GroupQuerySetMixin, generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.get_group_queryset()

    def get(self, request, pk):
        group = get_object_or_404(self.get_queryset(), pk=pk)
        all_time = request.query_params.get('all')
        month_param = request.query_params.get('month')

        lessons = Lesson.objects.filter(group=group)

        if all_time != 'true':
            if month_param:
                try:
                    year, month = map(int, month_param.split('-'))
                except ValueError:
                    return Response({'error': 'Неверный формат. Используйте YYYY-MM.'}, status=400)
            else:
                today = date.today()
                year, month = today.year, today.month
            lessons = lessons.filter(date__year=year, date__month=month)

        lessons = lessons.order_by('date')

        records = (
            LessonRecord.objects
            .filter(lesson__in=lessons)
            .select_related('student', 'lesson')
        )
        students = (
            StudentProfile.objects
            .filter(group=group)
            .select_related('user')
        )

        records_by_student = defaultdict(list)
        for record in records:
            records_by_student[record.student_id].append(record)

        students_data = []
        for student in students:
            student_records = records_by_student.get(student.pk, [])
            grades_by_date = {}
            total, count, late_count, total_late_min = 0, 0, 0, 0

            for r in student_records:
                grades_by_date[str(r.lesson.date)] = {
                    'grade': r.grade,
                    'attendance': r.attendance,
                    'late_minutes': r.late_minutes,
                }
                if r.attendance == 'late':
                    late_count += 1
                    total_late_min += r.late_minutes or 0
                if r.attendance == 'absent':
                    continue
                grade_str = r.grade.replace('+', '').replace('-', '')
                if grade_str.isdigit():
                    total += int(grade_str)
                    count += 1

            students_data.append({
                'full_name': student.user.get_full_name(),
                'total_grade': total,
                'average_grade': round(total / count, 2) if count > 0 else 0,
                'visit_count': count,
                'late_count': late_count,
                'total_late_minutes': total_late_min,
                'grades': grades_by_date,
            })

        return Response({
            'group': group.course_name,
            'start_date': group.created_at.isoformat() if group.created_at else None,
            'end_date': group.end_date.isoformat() if group.end_date else None,
            'lessons': [str(l.date) for l in lessons],
            'students': students_data,
        })


class MoveStudentAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        student_id = request.data.get('student_id')
        new_group_id = request.data.get('group_id')

        if not student_id or not new_group_id:
            return Response({'error': 'Укажите student_id и group_id.'}, status=400)

        student = get_object_or_404(StudentProfile, pk=student_id)
        new_group = get_object_or_404(Group, pk=new_group_id)

        if student.group_id == new_group.pk:
            return Response({'error': 'Студент уже в этой группе.'}, status=400)

        old_group_name = str(student.group)
        student.group = new_group
        student.save()

        return Response({
            'student': student.user.get_full_name(),
            'from_group': old_group_name,
            'to_group': str(new_group),
        })


class MonthlyReportListAPIView(generics.ListAPIView):
    serializer_class = MonthlyReportSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return MonthlyReport.objects.all()
        if hasattr(user, 'studentprofile'):
            return MonthlyReport.objects.filter(student=user.studentprofile)
        if hasattr(user, 'mentorprofile'):
            return MonthlyReport.objects.filter(group__mentor=user.mentorprofile)
        return MonthlyReport.objects.none()
