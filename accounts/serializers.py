from rest_framework import serializers
from .models import User, TeacherProfile, StudentProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone_number', 'email', 'role', 'profile_image', 'is_active', 'created_at', 'updated_at']


class TeacherProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = TeacherProfile
        fields = ['id', 'user', 'assigned_classes', 'qualification', 'subject_specialization']


class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = StudentProfile
        fields = ['id', 'user', 'roll_number', 'school_class', 'section', 'parent_phone']
