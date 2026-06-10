from rest_framework import serializers
from .models import User, TeacherProfile, StudentProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'phone_number', 'email', 
            'role', 'profile_image', 'is_active', 'created_at', 'updated_at'
        ]


class TeacherProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherProfile
        fields = [
            'id', 'employee_id', 'qualification', 'designation', 
            'experience', 'assigned_classes', 'assigned_subjects'
        ]


class StudentProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProfile
        fields = [
            'id', 'roll_number', 'father_name', 'mother_name', 
            'gender', 'date_of_birth', 'school_class', 'section', 
            'parent_phone', 'admission_date'
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    teacher_profile = TeacherProfileSerializer(required=False)
    student_profile = StudentProfileSerializer(required=False)

    class Meta:
        model = User
        fields = [
            'id', 'username', 'full_name', 'phone_number', 'email', 
            'role', 'profile_image', 'teacher_profile', 'student_profile'
        ]
        read_only_fields = ['id', 'username', 'role']

    def update(self, instance, validated_data):
        teacher_data = validated_data.pop('teacher_profile', None)
        student_data = validated_data.pop('student_profile', None)

        # Update core user fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update profiles depending on user role
        if instance.role == 'teacher' and teacher_data:
            profile, _ = TeacherProfile.objects.get_or_create(user=instance)
            for attr, value in teacher_data.items():
                if attr in ['assigned_classes', 'assigned_subjects']:
                    getattr(profile, attr).set(value)
                else:
                    setattr(profile, attr, value)
            profile.save()
        elif instance.role == 'student' and student_data:
            profile, _ = StudentProfile.objects.get_or_create(user=instance)
            for attr, value in student_data.items():
                setattr(profile, attr, value)
            profile.save()

        return instance
