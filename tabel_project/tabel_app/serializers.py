from rest_framework import serializers
from .models import (Admin, MentorProfile, StudentProfile, Group,
                     Lesson, LessonRecord)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"],
        )
        if user and user.is_active:
            attrs["user"] = user
            return attrs
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        user = instance["user"]
        refresh = RefreshToken.for_user(user)
        return {
            "user": {
                "username": user.username,
                "email": user.email,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class AdminListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['full_name']

class AdminDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = '__all__'

class MentorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MentorProfile
        fields = '__all__'


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'parent_name', 'parent_phone']


class LessonRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonRecord
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    lesson_list = LessonRecordSerializer(read_only=True, many=True)
    class Meta:
        model = Lesson
        fields = '__all__'


class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class GroupDetailSerializer(serializers.ModelSerializer):
    lesson_group = LessonSerializer(read_only=True, many=True)
    class Meta:
        model = Group
        fields = '__all__'