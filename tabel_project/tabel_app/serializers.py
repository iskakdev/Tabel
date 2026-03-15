from rest_framework import serializers
from .models import MentorProfile, StudentProfile, Group, Lesson, LessonRecord, MonthlyReport
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if user and user.is_active:
            attrs['user'] = user
            return attrs
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        user = instance['user']
        refresh = RefreshToken.for_user(user)
        return {
            'user': {'username': user.username, 'email': user.email},
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class MentorProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = MentorProfile
        fields = ['id', 'user', 'full_name']


class StudentProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'full_name', 'group']


class StudentProfileAdminSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'full_name', 'parent_name', 'parent_phone', 'group']


class LessonRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRecord
        fields = '__all__'

    def validate(self, attrs):
        if attrs.get('attendance') == 'late' and not attrs.get('late_minutes'):
            raise serializers.ValidationError(
                {'late_minutes': 'Укажите количество минут опоздания.'}
            )
        return attrs


class LessonSerializer(serializers.ModelSerializer):
    records = LessonRecordSerializer(read_only=True, many=True)

    class Meta:
        model = Lesson
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class MonthlyReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyReport
        fields = '__all__'