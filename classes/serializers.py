from rest_framework import serializers
from .models import SchoolClass
from accounts.serializers import UserSerializer
from schools.serializers import SchoolSerializer, AcademicSessionSerializer


class SchoolClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'section', 'class_teacher', 'school', 'session', 'created_at', 'updated_at']


class SchoolClassDetailSerializer(serializers.ModelSerializer):
    class_teacher = UserSerializer(read_only=True)
    school = SchoolSerializer(read_only=True)
    session = AcademicSessionSerializer(read_only=True)

    class Meta:
        model = SchoolClass
        fields = ['id', 'name', 'section', 'class_teacher', 'school', 'session', 'created_at', 'updated_at']
